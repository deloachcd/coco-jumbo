def user_input_answer(question):
    response = input(question)
    return response == "" or "y" in response


def exit_if_user_says_no(question):
    question = "{} [y/n] ".format(question)
    if user_input_answer(question):
        pass
    else:
        print("Exiting.")
        exit()


def _get_user_selection_from_queried_rows(
        queried_rows,
        multiple_select_allowed=False
):
    from lazy_modules.share.login_table_helpers import (
        render_table
    )

    if len(queried_rows) > 1:
        print(render_table(queried_rows, number_rows=True))
        user_selection = input(
            "Which entry would you like to select? [1-{}{}] ".format(
                len(queried_rows),
                ", or '*' for all" if multiple_select_allowed else ""
            )
        )
    elif len(queried_rows) == 1:
        user_selection = '1'
    else:
        print("No entries found in login table for query. Exiting.")
        exit()

    return user_selection


def execute_function_on_user_selected_row(
    queried_rows,
    function_to_execute
):
    user_selection = _get_user_selection_from_queried_rows(queried_rows)
    if (
        user_selection.isnumeric()
        and int(user_selection) >= 1
        and int(user_selection) <= len(queried_rows)
    ):
        row = queried_rows[int(user_selection) - 1]
        return function_to_execute(row)
    else:
        print("Invalid selection specified. Exiting.")
        exit()

# RQMW:
# 1. read login table from filesystem
# 2. query table from user input
# 3. modify table from query
# 4. write modified table to filesystem


def user_modify_table(
        table,
        queried_rows,
        action_verb,
        single_modify_function,    # actually mutates
        multiple_modify_function,  # returns modified copy
        prompt_for_confirmation=False
):
    from lazy_modules.share.login_table_helpers import (
        get_queried_row_index
    )

    user_selection = _get_user_selection_from_queried_rows(
        queried_rows,
        multiple_select_allowed=True
    )

    if user_selection == '*':
        # modify all rows matched by the query
        if prompt_for_confirmation:
            exit_if_user_says_no(
                "Do you really want to {} all {} records?".format(
                    action_verb, len(queried_rows))
            )
        table = multiple_modify_function(table)
        print(
            "Modified {} entries in login table.".format(
                len(queried_rows)
            )
        )
    elif (
            user_selection.isnumeric() and
            int(user_selection) >= 1 and
            int(user_selection) <= len(queried_rows)
    ):
        selection_index = int(user_selection)-1
        queried_row = queried_rows[selection_index]
        if prompt_for_confirmation:
            exit_if_user_says_no(
                "Really {} entry with login '{}' for platform '{}'?".format(
                    action_verb, queried_row[1], queried_row[0]
                )
            )
        single_modify_function(table, get_queried_row_index(queried_row))
        print(
            "Modified a single entry in login table.".format(
                len(queried_rows)
            )
        )
    else:
        print("Invalid entry specified for modification, exiting.")
        exit()

    return table
