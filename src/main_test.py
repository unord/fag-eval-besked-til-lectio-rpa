import datetime
from src import main as m

final_choice_date = "16/12-2022 09:00" # format: dd/mm/yyyy hh:mm
final_reg_date = "1/12-2022 09:00" # format: dd/mm/yyyy hh:mm
final_choice_date = datetime.datetime.strptime(final_choice_date, "%d/%m-%Y %H:%M")
final_reg_date = datetime.datetime.strptime(final_reg_date, "%d/%m-%Y %H:%M")


def main():
    now = datetime.datetime.now()
    # format now to match final_choice_date
    now = now.strftime("%d/%m-%Y %H:%M")
    now = datetime.datetime.strptime(now, "%d/%m-%Y %H:%M")

    final_reg_date_complete = m.final_reg_date_complete_state(now, final_reg_date)

    # Test to see if final completion datetime has passed
    if now > final_choice_date:
        print("Final datetime has passed.")
    # Test to see if final reg datetime has passed
    elif now > final_reg_date and final_reg_date_complete == False:
        print("Doing scheduels as ordered")

    else:
        print("Sending schedueled evals")
        print(f'Now: {now}')
        print(f'Now: {type(now)}')
        print(f'Final reg date: {final_reg_date}')
        print(f'Final reg date type: {type(final_reg_date)}')
        print(f'Final reg date complete: {final_reg_date_complete}.Is now({now}) > final_reg_date({final_reg_date}): {now > final_reg_date}')




if __name__ == '__main__':
    main()
