from classes.scrapper import Scrapper



def main():
    scrapper = Scrapper()
    #scrapper.get_current_activities()
    scrapper.get_history_data(last_day=1, last_month=4, last_year=2024)


if __name__ == "__main__":
    main()
