import json 
import csv
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('json_file',type=str, help= 'json text file')
    parser.add_argument('human_file',type=str, help= 'Human readable text file')
    args = parser.parse_args()
    arrs = []
    #read human readable file to get zebra ids
    zebra_ids = {}
    elephant_ids = {}
    lion_ids = {}
    with open(args.human_file) as f:
        for line in f:
            if 'Zebra' in line:
                id = line.split('-')[1].split(' ')[0]
                zebra_ids[id] = int(id)
            elif 'Elephant' in line:
                id = line.split('-')[1].split(' ')[0]
                elephant_ids[id] = int(id)
            elif 'Lion' in line:
                id = line.split('-')[1].split(' ')[0]
                lion_ids[id] = int(id)
    # read text file
    with open(args.json_file) as f:
        for line in f:
            if line == "":
                continue
            try:
                arr = json.loads(line)
                arrs.append(arr)
            except:
                continue
    # output animals to csv file
    with open('data.csv','w',encoding='UTF8') as csv_file:
        writer = csv.writer(csv_file)
        header = ['id','type','timestamp','oxygen','heartrate','locationX','locationY','temperature','humidity']
        writer.writerow(header)
        animals = []
        for arr in arrs:
            for animal in arr:
                id = animal['deviceId'].split('_')[1]
                animal_type = None
                if id in zebra_ids:
                    animal_type = 'Zebra'
                elif id in lion_ids:
                    animal_type = 'Lion'
                elif id in elephant_ids:
                    animal_type = 'Elephant'
                timestamp = animal['timestamp']
                oxygen = None
                heartrate = None
                locationX = None
                locationY = None
                temperature = None
                humidity = None
                sensors = animal['sensors']
                for sensor in sensors:
                    # pulseOxygen
                    if sensor['type'] == 31:
                        oxygen = sensor['input']['pulseOxygen'][1]
                        heartrate = sensor['input']['pulseOxygen'][0]
                    # location
                    elif sensor['type'] == 27:
                        locationX = sensor['input']['location'][0]
                        locationY = sensor['input']['location'][1]
                    # temperature
                    elif sensor['type'] == 24:
                        temperature = sensor['input']['temperature']
                    # humidity
                    elif sensor['type'] == 25:
                        humidity = sensor['input']['humidity']
                # input row into csv
                row = [id,animal_type,timestamp,oxygen,heartrate,locationX,locationY,temperature,humidity]
                writer.writerow(row)

if __name__ == "__main__":
    try:
        main()
    finally:
        print("parsing complete")