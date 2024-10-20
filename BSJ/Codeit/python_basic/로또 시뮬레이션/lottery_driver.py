import lottery

HEAD_HTML = '''
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>로또</title>

    <style type="text/css" media="screen">
        body {
            background-color: #FAFAFA;
            padding-top: 80px;
        }

        .navbar {
            background-color: #29B895;
            border-radius: 0 !important;
        }

        .navbar-brand {
            color: white;
        }

        .navbar-brand:hover {
            color: white;
        }

        .jumbotron {
            border-radius: 10px;
            padding: 20px;
        }

        .jumbotron h1 {
            margin: 0 0 20px 0;
            font-size: 24px !important;
        }

        .cash-div {
            font-size: 24px;
        }

        .cash-div b {
            margin-right: 10px;
        }

        .red {
            background-color: #D84134;
            color: white;
        }

        .green {
            background-color: #6AC83B;
        }

        .yellow {
            background-color: #FBC34B;
        }

        .blue {
            background-color: #528FD2;
            color: white;
        }

        .black {
            background-color: #414141;
        }

        .plus {
            font-size: 30px;
            margin: 0 10px 0 10px;
        }

        .ball {
            color: white;
            font-size: 20px;
            border-radius: 50%;
            display: inline-block;
            width: 60px;
            height: 60px;
            text-align: center;
            line-height: 60px;
        }

        .attempt-numbers {
            font-size: 18px;
            outline: 1px solid black;
            display: inline-block;
            margin-bottom: 20px;
            margin-right: 20px;
            height: 30px;
        }

        .attempt-number {
            display: inline-block;
            width: 30px;
            text-align: center;
            line-height: 30px;
        }

        .attempt-prize {
            display: inline-block;
            font-size: 18px;
        }
    </style>

    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">

    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">

    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
</head>
'''

MAIN_HTML = '''
<!DOCTYPE html>
<html>
    <body>
        <nav class="navbar navbar-fixed-top">
            <div class="container-fluid">
                <!-- Brand and toggle get grouped for better mobile display -->
                <div class="navbar-header">
                    <a class="navbar-brand" href="#">LOTTO</a>
                </div>
            </div><!-- /.container-fluid -->
        </nav>

        <div class="col-xs-10 col-xs-offset-1">
            <div class="jumbotron">
                <h1><b>당첨 번호</b></h1>
                {numbers}
            </div>
        </div>

        <div class="col-xs-5 col-xs-offset-1">
            <div class="jumbotron cash-div">
                <b>당첨 금액</b>
                <span>‎₩{total_prize}</span>
            </div>
        </div>

        <div class="col-xs-5">
            <div class="jumbotron cash-div">
                <b>쓴 금액</b>
                <span>‎₩{total_cost}</span>
            </div>
        </div>

        <div class="col-xs-10 col-xs-offset-1">
            <div class="jumbotron">
                <h1><b>내 번호</b></h1>
                {attempts}
            </div>
        </div>

        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <!-- Include all compiled plugins (below), or include individual files as needed -->
    </body>
</html>
'''


def get_color(number):
    if number <= 10:
        return "yellow"
    elif number <= 20:
        return "blue"
    elif number <= 30:
        return "red"
    elif number <= 40:
        return "black"
    else:
        return "green"


def generate_numbers_html(numbers):
    # template for winning ball
    ball_html = '''
    <div class="ball {color}">
        {number}
    </div>
    '''

    html = ""
    for number in numbers[:6]:
        html += ball_html.format(number = number, color = get_color(number))
    html += '<span class="plus">+</span>'
    html += ball_html.format(number = numbers[-1], color = get_color(numbers[-1]))
    return html


def generate_attempt_html(attempt, winning_numbers):
    number_html = '''
    <span class="attempt-number">{number}</span>
    '''

    red_number_html = '''
    <span class="attempt-number red">{number}</span>
    '''

    blue_number_html = '''
    <span class="attempt-number blue">{number}</span>
    '''

    attempt_html = ""
    for num in attempt[0]:
        if num in winning_numbers[:6]:
            attempt_html += red_number_html.format(number=num)
        elif num in winning_numbers[6:]:
            attempt_html += blue_number_html.format(number=num)
        else:
            attempt_html += number_html.format(number=num)

    html = '''
    <div class="attempt">
        <div class="attempt-numbers">
            {attempt}
        </div>
        <div class="attempt-prize">
            ‎₩{prize}
        </div>
    </div>
    '''.format(attempt=attempt_html, prize=attempt[1])
    return html


def main(winning_numbers, tries, total_prize, total_cost):
    out_file = open('./Codeit/로또 시뮬레이션/lottery.html', 'w', encoding='utf-8')

    winning_numbers_html = generate_numbers_html(winning_numbers)

    attempts_html = ""

    for attempt in tries:
        attempts_html += generate_attempt_html(attempt, winning_numbers)

    out_file.write(HEAD_HTML + MAIN_HTML.format(
        numbers=winning_numbers_html,
        attempts=attempts_html,
        total_prize=total_prize,
        total_cost=total_cost)
    )
    out_file.close()


WINNING_NUMBERS = lottery.draw_winning_numbers()
NUM_TRIES = 100

tries = []
total_prize = 0
total_cost = 0

for i in range(NUM_TRIES):
    attempt = sorted(lottery.generate_numbers(6))
    prize = lottery.check(attempt, WINNING_NUMBERS)
    tries.append((attempt, prize))

    total_prize += prize
    total_cost += 1000

main(
    WINNING_NUMBERS,
    sorted(tries, key=lambda x: -x[1]),
    total_prize,
    total_cost
)
