from classes.scrapper import Scrapper


def main():
    scrapper = Scrapper()
    scrapper.get_history_data(last_day=3, last_month=6, last_year=2024)
    scrapper.export_data_to_csv()

if __name__ == "__main__":
    main()
