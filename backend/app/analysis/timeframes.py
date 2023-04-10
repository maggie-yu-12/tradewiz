from datetime import date

from dateutil.relativedelta import relativedelta

####################################################################
# NOTE: We need to strictly define the 'to_date', as well as from. #
####################################################################


def get_week_ago_range():
    # calculate 6 months ago from today
    today = date.today() + relativedelta(
        days=-1
    )  # subtracting one as we are going from 2/19/23 instead of 2/20/23 to keep it consistent for this week

    # calculate last week and the week before if needed
    today_formatted = today.strftime("%Y%m%d%H%M")
    last_week_formatted_7 = (today + relativedelta(weeks=-1)).strftime("%Y%m%d%H%M")
    last_week_formatted_6 = (today + relativedelta(days=-6)).strftime("%Y%m%d%H%M")
    last_week_formatted_5 = (today + relativedelta(days=-5)).strftime("%Y%m%d%H%M")
    last_week_formatted_4 = (today + relativedelta(days=-4)).strftime("%Y%m%d%H%M")
    last_week_formatted_3 = (today + relativedelta(days=-3)).strftime("%Y%m%d%H%M")
    last_week_formatted_2 = (today + relativedelta(days=-2)).strftime("%Y%m%d%H%M")
    last_week_formatted_1 = (today + relativedelta(days=-1)).strftime("%Y%m%d%H%M")

    return {
        "dates_since": [
            last_week_formatted_7,
            last_week_formatted_6,
            last_week_formatted_5,
            last_week_formatted_4,
            last_week_formatted_3,
            last_week_formatted_2,
            last_week_formatted_1,
        ],
        "dates_until": [
            last_week_formatted_6,
            last_week_formatted_5,
            last_week_formatted_4,
            last_week_formatted_3,
            last_week_formatted_2,
            last_week_formatted_1,
            today_formatted,
        ],
    }


def get_two_weeks_ago_range():
    # calculate 6 months ago from today
    today = date.today() + relativedelta(
        days=-1
    )  # subtracting one as we are going from 2/19/23 instead of 2/20/23 to keep it consistent for this week

    # calculate last week and the week before if needed
    today_formatted = today.strftime("%Y%m%d%H%M")
    two_weeks_formatted_14 = (today + relativedelta(weeks=-2)).strftime("%Y%m%d%H%M")
    two_weeks_formatted_13 = (today + relativedelta(days=-6)).strftime("%Y%m%d%H%M")

    return {
        "dates_since": [
            two_weeks_formatted_14,
        ],
        "dates_until": [
            two_weeks_formatted_13,
        ],
    }


def get_one_month_ago_range():
    # calculate 6 months ago from today
    today = date.today() + relativedelta(
        days=-1
    )  # subtracting one as we are going from 2/19/23 instead of 2/20/23 to keep it consistent for this week

    today_formatted = today.strftime("%Y%m%d%H%M")

    # calculate last month
    last_month_start_date_28 = (today + relativedelta(weeks=-4)).strftime("%Y%m%d%H%M")
    last_month_start_date_27 = (today + relativedelta(days=-27)).strftime("%Y%m%d%H%M")
    last_month_start_date_26 = (today + relativedelta(days=-26)).strftime("%Y%m%d%H%M")
    last_month_start_date_25 = (today + relativedelta(days=-25)).strftime("%Y%m%d%H%M")
    last_month_start_date_24 = (today + relativedelta(days=-24)).strftime("%Y%m%d%H%M")

    return_val = {}
    since_dates = []
    until_dates = []
    # for i in range(28, 0, -1):
    #     start_date = (today + relativedelta(weeks=-i)).strftime("%Y%m%d%H%M")
    #     since_dates.append(start_date)
    #     if i == 1:
    #         until_dates.append(today_formatted)
    #     elif i < 28:
    #         until_dates.append(start_date)

    return {
        "dates_since": [
            last_month_start_date_28,
            last_month_start_date_27,
            last_month_start_date_26,
            last_month_start_date_25,
            last_month_start_date_24,
        ],
        "dates_until": [
            last_month_start_date_27,
            last_month_start_date_26,
            last_month_start_date_25,
            last_month_start_date_24,
            today_formatted,
        ],
    }


def get_six_months_ago_range():
    # calculate 6 months ago from today
    today = date.today() + relativedelta(
        days=-1
    )  # subtracting one as we are going from 2/19/23 instead of 2/20/23 to keep it consistent for this week

    today_formatted = today.strftime("%Y%m%d%H%M")

    six_months = today + relativedelta(months=-6)
    six_months_formatted = six_months.strftime("%Y%m%d%H%M")
    six_months_formatted_start_date = (six_months + relativedelta(weeks=-1)).strftime(
        "%Y%m%d%H%M"
    )

    return [today_formatted, six_months_formatted]
