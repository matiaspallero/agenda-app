def format_date(date):
    return date.strftime("%d-%m-%Y")

def validate_input(input_value, valid_options):
    return input_value in valid_options

def print_separator():
    print("-" * 30)