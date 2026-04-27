from datetime import date


def today(request):
    return {"date_today": date.today().isoformat()}
