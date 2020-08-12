import os
from obspy import read, read_inventory

""" corrects the intrument response of raw waveform data """
#get the instrument response corrections xml file
inventory = read_inventory("inv.xml", format="STATIONXML")
pre_filt = (0.005,0.01,8,10)

#add the mseed files to a stream
for file in os.listdir(os.getcwd()):
    if file.split(".")[-1] == "MSEED":
        print(file)
        try:
            st += read(file)
        except:
            st = read(file)

st.merge()
st.plot()

#Performt he correction
st.attach_response(inventory)
st.remove_response(output="VEL", water_level=60, pre_filt=pre_filt, zero_mean=True,taper=True, taper_fraction=0.05,plot=True)

#save corrected data
for tr in st:
    tr.write(tr.stats.station+'.'+tr.stats.network+'.'+tr.stats.location+'.'+tr.stats.channel+".IRC.MSEED",format="MSEED")
st.plot()
