
# You should not modify this part.
def config():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--consumption", default="./sample_data/consumption.csv", help="input the consumption data path")
    parser.add_argument("--generation", default="./sample_data/generation.csv", help="input the generation data path")
    parser.add_argument("--bidresult", default="./sample_data/bidresult.csv", help="input the bids result path")
    parser.add_argument("--output", default="output.csv", help="output the bids path")

    return parser.parse_args()


def output(path, data):
    import pandas as pd

    df = pd.DataFrame(data, columns=["time", "action", "target_price", "target_volume"])
    df.to_csv(path, index=False)

    return

def write_csv(file_name, output):
    import csv
    with open(file_name,'a',newline='') as csvfile:
        csv_write=csv.writer(csvfile)
        
        for i in output:
            csv_write.writerow([i])
    #print("Csv file is writed!")

def get_time():
    import datetime
    
    today = datetime.date.today()
    output = []
    for hour in range(24):
        dt = datetime.time(hour, 0, 0)
        date_time = today.strftime("%Y-%m-%d") + dt.strftime(" %H:%M:%S")
        output.append(date_time)
    
    return output

if __name__ == "__main__":
    args = config()
    '''
    data = [["2018-01-01 00:00:00", "buy", 2.5, 3],
            ["2018-01-01 01:00:00", "sell", 3, 5]]
    '''
    record = []
    date_time = get_time()
    for i in date_time:
        data = [[i , "buy", 2.5, 3],
                [i , "sell", 3, 5]]
        for act in data:
            record.append(act)
        
    output(args.output, record)