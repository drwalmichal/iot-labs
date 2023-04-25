import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse


def lions_zebras_elephants(df):
    z_df = df[df['type'] == 'Zebra']
    l_df = df[df['type'] == 'Lion']
    e_df = df[df['type']== 'Elephant']
    # assign colors
    e_df = e_df.assign(color='purple')
    z_df = z_df.assign(color='blue')
    l_df = l_df.assign(color='red')
    # assign size of markers
    e_df = e_df.assign(size=100)
    z_df = z_df.assign(size=20)
    l_df = l_df.assign(size=50)
    # plot
    zebras = plt.scatter(z_df['locationX'],z_df['locationY'],c=z_df['color'],s=z_df['size'])
    lions = plt.scatter(l_df['locationX'],l_df['locationY'],c=l_df['color'],s=l_df['size'])
    elephants = plt.scatter(e_df['locationX'],e_df['locationY'],c=e_df['color'],s=e_df['size'])
    plt.legend((zebras,lions,elephants),('Zebras','Lions','Elephants'))
    plt.title('Zebra, Lion, and Elephant Locations')
    plt.xlabel('X coord')
    plt.ylabel('Y coord')
    plt.show()

def zebras(df):
    df = df[df['type'] == 'Zebra']
    plt.scatter(df['locationX'],df['locationY'],c=df['id'])
    plt.title('Zebra Locations')
    plt.xlabel("X coord")
    plt.ylabel('Y coord')
    plt.show()

def oxygen_v_time(df):
    df = df[df['type']=='Zebra']
    plt.scatter(df['timestamp'],df['oxygen'])
    plt.title('Oxygen Saturation (SpO2 %) v Time (microseconds)')
    plt.xlabel('Time (microseconds)')
    plt.ylabel('Oxygen Saturation (SpO2 %)')
    plt.show()

def heartrate_v_time(df):
    plt.scatter(df['timestamp'],df['heartrate'])
    plt.title('Heart Rate (bpm) v Time (microseconds)')
    plt.xlabel('Time (microseconds)')
    plt.ylabel('Heart Rate (bpm)')
    plt.show()

def cdf(df):
    df = df[df['type']=='Zebra']
    cdf = pd.DataFrame()
    # loop through all zebras by id
    for id in df['id'].unique():
        z_df = df[df['id'] == id]
        #sort by increasing timestamp
        z_df.sort_values(by=['timestamp'],ascending=[True])
        z_df = z_df[['timestamp','locationX','locationY']]
        z_df = z_df.diff().fillna(0)
        z_df['distance'] = np.sqrt(z_df['locationX']**2 + z_df['locationY']**2)
        z_df['speed'] = (z_df['distance']/z_df['timestamp']).fillna(0)
        z_df = z_df[['speed']]
        cdf = cdf.append(z_df,ignore_index=True)
    cdf = cdf['speed'].value_counts().sort_index().cumsum()/len(cdf)
    plt.plot(cdf.index,cdf)
    plt.title('CDF v Speed (cm/microsecond)')
    plt.xlabel('Speed (cm/microsecond)')
    plt.ylabel('CDF')
    plt.show()

FUNCTION_MAP = {'scatter_zebras': zebras,
                'scatter_all': lions_zebras_elephants,
                'oxygen_v_time':oxygen_v_time,
                'heartrate_v_time':heartrate_v_time,
                'cdf':cdf}
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command',choices=FUNCTION_MAP.keys(),help='The function you want to call')
    args = parser.parse_args()
    # read in csv file
    df = pd.read_csv('data.csv')
    func = FUNCTION_MAP[args.command]
    func(df)

if __name__ == "__main__":
    try:
        main()
    finally:
        print('visualizations complete')