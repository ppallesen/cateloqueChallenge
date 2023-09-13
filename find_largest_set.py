from ortools.sat.python import cp_model


def find_potential_pieces(users, min_n):
    # Excluding all posible pieces where less than half of the people
    # have them. Also taking account of the quantity. Such that if 80 %
    # has 1 of a curtain piece, but only 40 % has 2, then it is not
    # nesseary to consider taking more than one of these pieces in the set
    piece_sets = {}
    for user in users:
        for piece_set in user.piece_sets:
            match_id = piece_set.match_id
            if match_id not in piece_sets:
                piece_sets[match_id] = [piece_set]
            else:
                piece_sets[match_id].append(piece_set)
    return {
        match_id: sorted(piece_set_list, key=lambda x: x.quantity)[-min_n].quantity
        for match_id, piece_set_list in piece_sets.items()
        if len(piece_set_list) >= min_n
    }


def find_largest_possible_set_that_most_can_build(users, p: float = 0.5):
    min_n = int(len(users) * p)
    assert min_n
    potential_piece_count = find_potential_pieces(users, min_n)
    if not potential_piece_count:
        return {}

    model = cp_model.CpModel()
    pieces_selected_variables = {}
    for match_id, quantity in potential_piece_count.items():
        variables = [
            model.NewIntVar(0, 1, str(match_id) + str(i)) for i in range(quantity)
        ]
        for i in range(quantity - 1):
            # if you take the second of a piece in the set you also need to the first piece
            model.Add(variables[i] >= variables[i + 1])
        pieces_selected_variables[match_id] = variables

    #
    users_that_cant_assemble_the_set_variables = {
        user.id: model.NewIntVar(0, 1, str(user.id)) for user in users
    }

    # Ensure that if one piece is missing then user can't count as a user
    # that can build the set
    for user in users:
        user_cant_assemble_var = users_that_cant_assemble_the_set_variables[user.id]
        pieces_count_user = {
            piece_set.match_id: piece_set.quantity for piece_set in user.piece_sets
        }
        for (
            match_id,
            pieces_selected_variable_list,
        ) in pieces_selected_variables.items():
            if match_id in pieces_count_user:
                if pieces_count_user[match_id] < len(pieces_selected_variable_list):
                    # We are considering taking 3 of these pieces but this user has only
                    # instance. Then That user can't build the set if two pieces are selected
                    for var in pieces_selected_variable_list[
                        pieces_count_user[match_id] :
                    ]:
                        model.AddImplication(var, user_cant_assemble_var)
            else:
                # If user does not have any of the pieces the user cant assemble the set
                for var in pieces_selected_variable_list:
                    model.AddImplication(var, user_cant_assemble_var)

    # There must be at least min_n users that can assemble the set
    model.Add(
        sum(users_that_cant_assemble_the_set_variables.values()) <= (len(users) - min_n)
    )

    # maximize the pieces selected
    model.Maximize(
        sum(var for var_list in pieces_selected_variables.values() for var in var_list)
    )

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = {}
        for match_id, var_list in pieces_selected_variables.items():
            quantity = sum(solver.Value(var) for var in var_list)
            if quantity:
                solution[match_id] = quantity
        return solution
    else:
        raise Exception("Bug in the code solver could not solve")
