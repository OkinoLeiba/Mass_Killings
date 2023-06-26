# %% [markdown]
# 
# <img src="https://s.abcnews.com/images/US/gun-flag-abc-ps2-211020_1634760470451_hpMain_2_16x9_1600.jpg" alt="Gun Violence Protest"  style="width: 71px; height: 40px; padding-bottom: 0px;"></img>
# 
# <hr style="margin-bottom: 5px; border-color: gray;"></hr>
# 
# <p style="display: flex; overflow-wrap: wrap: left; text-align: left; color: #b2c2bf;">Despite it prevalence in the media, mass shootings are statistically rare events, representing an availability bias, and give the impression that these events are common. Coupled with the psychological trauma and nature of the incidents being the violent loss of life, person can feel as if the world is on fire, but incidents of homicide or accidental shootings are more prevalent. What is clear based on statistical science is that mass shootings are increasing in both frequency and the number of victims. This can be constituted as a public health crisis given the scale of increase and nature of the incident in the ability of certain type of firearms to cause a significant amount of damage with a short period of time.</p>
# 
# <!-- [gun_flag](https://s.abcnews.com/images/US/gun-flag-abc-ps2-211020_1634760470451_hpMain_2_16x9_1600.jpg) -->
# 
# 
# <!-- ![us_gun](https://www.washingtonpost.com/resizer/JXTDtmbZjrw0Lp0KkoICNThn560=/arc-anglerfish-washpost-prod-washpost/public/IQY6ZWRMJFFXVL642XBSIYETG4.png) -->
# 
# <!-- <img src="https://www.washingtonpost.com/resizer/JXTDtmbZjrw0Lp0KkoICNThn560=/arc-anglerfish-washpost-prod-washpost/public/IQY6ZWRMJFFXVL642XBSIYETG4.png" alt="Gun Violence Protest"  style="width: 710px; height: 400px; float: right; margin-left: 350px; position: absolute; z-index: -1;"></img> -->
# 
# 
# <img src="https://images.squarespace-cdn.com/content/v1/5b0376b58f5130630a44071a/bedb9621-cdf1-47d0-bfa1-afc086bab675/demonstrationforpeace.jpeg?format=1000w" alt="Gun Violence Protest"  style="width: 710px; height: 400px; float: right; margin-left: 350px;"></img>

# %% [markdown]
# # <span style="display: flex; justify-content: center; font-size: 40px; font-family: copperplate; font-weight: bold; color: #b2c2bf;">Mass Killings in America</span>

# %%
import pandas as pd, numpy as np, seaborn as sns, matplotlib.pyplot as plt, matplotlib as mlt, geopandas as gp, geodatasets
mlt.rcParams['axes.facecolor'] = "lightgray"


# %%
mk_incident_public = "https://query.data.world/s/f5axjxaynrhsg2qkkpgxjzoqbdvkat?dws=00000"
mkip_data = pd.read_table(mk_incident_public, delimiter=",", header=0, skipinitialspace=True, engine="python", encoding="utf-8", encoding_errors="strict", on_bad_lines="warn")
mkip_data.rename(str.title, axis="columns", inplace=True)
mkip_data.rename({"Incident_Id":"Incident_ID","Firstcod":"FirstCOD", "Secondcod":"SecondCOD" }, axis="columns", inplace=True)
mkip_data['FirstCOD'] = [s.title() for s in mkip_data['FirstCOD']]
mkip_data['Location_Type'] = [s.title() for s in mkip_data['Location_Type']]




# %%
mkip_data.head(3)

# %% [markdown]
# ## <span style="font-family: copperplate; font-weight: bold; color: #b2c2bf;">Exploratory Data Analysis</span>

# %%
mkip_data.tail(3)

# %%
mkip_data.index

# %%
mkip_data.shape

# %%
mkip_data.size

# %%
mkip_data.ndim

# %%
mkip_data.dtypes

# %%
mkip_data.columns

# %%
for ele in ['FirstCOD', 'SecondCOD','Type', 'Situation_Type', 'Location_Type', 'Location']:
    print(mkip_data[ele].unique())

# %%
mkip_data.info()

# %%
cat = mkip_data['FirstCOD'].unique()
c = mkip_data.groupby(mkip_data['FirstCOD']).FirstCOD.count()
duplicates = set()
# print(sum(1 for item in cat if all(item in mkip_data['FirstCod'])))
sum(1 for cat in mkip_data['FirstCOD'])

# %%
mkip_data.select_dtypes(include="object").nunique()

# %%
if not(any(mkip_data.notna())) or not(any(mkip_data.notnull())):
    print("All Good")
else:
    print("Work to be Done")

# %%
100 * mkip_data.isnull().sum() / mkip_data.shape[0]

# %% [markdown]
# ## <span style="font-family: copperplate; font-weight: bold; color: #b2c2bf;">Data Analysis and Visualization</span>

# %%
mkip_data[["Num_Offenders","Num_Victims_Killed","Num_Victims_Injured"]].describe().round()

# %%
print("Total Number of Mass Violence Incidents: ",  mkip_data.Incident_ID.sum())
print("Total Number of Victims: ",  mkip_data.Num_Victims_Killed.sum())
print("Total Number of Victims: ",  mkip_data.Num_Victims_Injured.sum())

# %%
mkip_data.groupby("Date", axis=0).filter(lambda x: (x.nunique() > 1).any()).iloc[:, 1:8]
# mkip_data["Same_Day"] = mkip_data.groupby("Date", axis=0).nunique()

# %% [markdown]
# ### <span style="font-family: copperplate; font-weight: bold; color: #b2c2bf;">Mass Violence by State</span>

# %%
state_count = mkip_data.groupby(["State"]).Incident_ID.count().sort_values(ascending=False)
state_num_victims = mkip_data.groupby(["State"]).Num_Victims_Killed.sum().sort_values(ascending=False)
print(state_num_victims)

# %%
from PIL import Image
plt.figure(figsize=(8,4), constrained_layout=True, dpi=120)
plt.imshow(np.asarray(Image.open('images.png')))

# %%
fig, axe = plt.subplots(figsize=(16,4), constrained_layout=False, dpi=120, facecolor="dimgray", label="Mass Violence by State")
state_count.plot.bar(color="ghostwhite")
axe.legend(labels=["Mass Violence Count"], loc="upper right", mode="none", title="Mass Violence by State")
axe.set_xlabel("State")
axe.set_title("Mass Violence by State")
axe.plot();

# %%
state_avg_victims = mkip_data.groupby(["State"]).Num_Victims_Killed.mean().sort_values(ascending=False).round()
state_avg_victims

# %%
fig, axe = plt.subplots(figsize=(16,4), constrained_layout=False, dpi=120, facecolor="dimgray", label="Mass Violence by State")
# state_avg_victims.plot.line(color="black")
state_avg_victims.plot.bar(color="ghostwhite")
axe.legend(labels=["Mass Violence Average"], loc="upper right", mode="none", title="Mass Violence by State")
axe.set_xlabel("State")
axe.set_title("Mass Violence by State")
axe.plot();

# %% [markdown]
# ### <span style="font-family: copperplate; font-weight: bold; color: #b2c2bf;">Mass Violence by Year</span>

# %%
mkip_data["Date_Year"] = pd.to_datetime(mkip_data["Date"], errors="coerce", yearfirst=True).dt.year
date_count = mkip_data.groupby(["Date_Year"]).Incident_ID.count()
print(date_count)

# %%
fig, axe = plt.subplots(figsize=(16,4), constrained_layout=False, dpi=120, facecolor="dimgray", label="Mass Violence by Year")
date_count.plot.bar(color="ghostwhite")
axe.legend(labels=["Mass Violence Count"], loc="upper right", mode="none", title="Mass Violence by Year")
axe.set_xlabel("Year")
axe.set_title("Mass Violence by Year")
axe.plot();

# %%
mkip_data["Date_Year"] = pd.to_datetime(mkip_data["Date"], errors="coerce", yearfirst=True).dt.year
date_mean = mkip_data.groupby(["Date_Year"]).Incident_ID.mean().round(1)
print(date_mean)

# %%
fig, axe = plt.subplots(figsize=(16,4), constrained_layout=False, dpi=120, facecolor="dimgray", label="Mass Violence by Year")
date_mean.plot.bar(color="ghostwhite")
axe.legend(labels=["Mass Violence Average"], loc="upper right", mode="none", title="Mass Violence by Year")
axe.set_xlabel("Year")
axe.set_title("Mass Violence by Year")
axe.plot();

# %%
roc_mean = date_mean.pct_change()

# %%
fig, axe = plt.subplots(figsize=(16,4), constrained_layout=False, dpi=120, facecolor="dimgray", label="Mass Violence by Year")
roc_mean.plot.bar(color="ghostwhite")
axe.legend(labels=["Mass Violence Rate of Change"], loc="upper right", mode="none", title="Mass Violence by Year")
axe.set_xlabel("Year")
axe.set_title("Mass Violence by Year")
axe.plot();

# %%
from bokeh.plotting import figure
from bokeh.io import output_notebook, show
output_notebook()

fig = figure(width=1500, height=500,  title="Mass Violence by Year")
fig.grid.grid_line_alpha=0.3
fig.xaxis.axis_label="Year"
fig.background_fill_color = "lightgray"
fig.vbar(x=date_count.index, top=date_count.values, color="black", width=0.7)

show(fig)



# %% [markdown]
# ### <span style="font-family: copperplate; font-weight: bold; color: #b2c2bf;">Mass Shoots by Type</span>

# %%
type_count= mkip_data.groupby(["Type"]).Incident_ID.count().sort_values(ascending=False)
print(type_count)


# %%
fig, axe = plt.subplots(figsize=(16,4), constrained_layout=False, dpi=120, facecolor="dimgray", label="Mass Violence by Type")
type_count.plot.barh(color="ghostwhite")
axe.legend(labels=["Mass Violence Count"], loc="upper right", mode="none", title="Mass Violence by Type")
axe.set_ylabel("Type of Violent Event")
axe.set_title("Mass Violence by Type")
axe.plot();

# %% [markdown]
# ### <span style="font-family: copperplate; font-weight: bold; color: #b2c2bf;">Mass Violence by Location</span>

# %%
location_count = mkip_data.groupby(["Location"]).Location.count().sort_values(ascending=False)
print(location_count)

# %%
fig, axe = plt.subplots(figsize=(16,4), constrained_layout=False, dpi=120, facecolor="dimgray", label="Mass Violence by Location")
location_count.plot.bar (color="ghostwhite")
axe.legend(labels=["Mass Violence Count"], loc="upper right", mode="none", title="Mass Violence by Location")
axe.set_xlabel("Location of Violent Event")
axe.set_title("Mass Violence by Location")
axe.plot();

# %% [markdown]
# ### <span style="font-family: copperplate; font-weight: bold; color: #b2c2bf;">Mass Violence by Location Type</span>

# %%
print(mkip_data["Location"].unique())
hashLoc = {
"Public" : ['Commercial/Retail', 'Bar/Club/Restaurant', 'School', 'Open space', 'Medical facility', 'Hotel/Motel',
'House of worship','Shelter/Drug house', 'College'],
"Non-Public" : ['Residence'],
"Other" : ['Multiple', 'Vehicle', 'Government/Transit']}
def replace_loc(mkip_data_loc):
    return "".join(key for key, values in hashLoc.items() for value in values if value in mkip_data_loc)

mkip_data["Type_Location"] = mkip_data["Location"].apply(replace_loc)


# %%
typeLoc_count = mkip_data.groupby(["Type_Location"]).Type_Location.count().sort_values(ascending=False)
print(typeLoc_count)

# %%
fig, axe = plt.subplots(figsize=(9,5), constrained_layout=False, dpi=120, facecolor="lightgray", label="Mass Violence by Type")
typeLoc_count.plot.bar(stacked=False, color="ghostwhite")
axe.set_xlabel("Location Type of Violent Event")
axe.set_title("Class of Location")
axe.plot();

# %%
fig, axe = plt.subplots(figsize=(10,9), constrained_layout=False, dpi=120, facecolor="lightgray", label="Mass Violence by Type")
typeLoc_count.plot.pie(stacked=False, cmap="mako")
axe.set_ylabel("Location Type of Violent Event")
axe.set_title("Class of Location")
axe.plot();

# %%
fig, axe = plt.subplots(figsize=(10,8), constrained_layout=False, dpi=120, facecolor="lightgray", label="Mass Violence by Type")
type_count.plot.pie(cmap="inferno")
axe.set_ylabel("Type of Violent Event")
axe.set_title("Mass Violence by Type")
axe.plot();

# %%
fig, axe = plt.subplots(figsize=(9,4), constrained_layout=False, dpi=120, facecolor="lightgray", label="Mass Violence by Type")
stack = mkip_data.groupby("FirstCOD")["FirstCOD",'Num_Offenders', 'Num_Victims_Killed', 'Num_Victims_Injured'].sum()
stack.rename({"Num_Offenders":"Num Offenders","Num_Victims_Killed":"Num Victims Killed", "Num_Victims_Injured":"Num Victims Injured" }, axis="columns", inplace=True)
stack.plot.bar(ax=axe, stacked=True, cmap="mako")
axe.set_xlabel("Cause of Death")
# axe.set_title("Class of Location")
axe.plot();



# %%
gdf = gp.GeoDataFrame(mkip_data, geometry=gp.points_from_xy(mkip_data.Longitude, mkip_data.Latitude), crs="EPSG:4326")
usa = gp.read_file(geodatasets.get_path('naturalearth.land'))
ax = usa.plot(figsize=(20,9), color="lightblue")
ax.set_axis_off()
gdf.plot(ax=ax, color="black")


# %%

mk_offenders_public = "https://query.data.world/s/di7bmak4rf6qkkmu2v64xfsei64y2j?dws=00000"
mkop_data = pd.read_table(mk_incident_public, delimiter=",", header=0, skipinitialspace=True, engine="python", encoding="utf-8", encoding_errors="strict", on_bad_lines="warn")
mkop_data.rename(str.title, axis="columns", inplace=True)
mkop_data.rename({"Incident_Id":"Incident_ID","Firstcod":"FirstCOD", "Secondcod":"SecondCOD" }, axis="columns", inplace=True)
mkop_data['FirstCOD'] = [s.title() for s in mkip_data['FirstCOD']]
mkop_data['Location_Type'] = [s.title() for s in mkip_data['Location_Type']]
mkop_data.head(1)

# %%
mk_victims_public = "https://query.data.world/s/zrk6mdov7k3wkg3sve4e6wylul746d?dws=00000"
mkvp_data = pd.read_table(mk_incident_public, delimiter=",", header=0, skipinitialspace=True, engine="python", encoding="utf-8", encoding_errors="strict", on_bad_lines="warn")
mkvp_data.rename(str.title, axis="columns", inplace=True)
mkvp_data.rename({"Incident_Id":"Incident_ID","Firstcod":"FirstCOD", "Secondcod":"SecondCOD" }, axis="columns", inplace=True)
mkvp_data['FirstCOD'] = [s.title() for s in mkip_data['FirstCOD']]
mkvp_data['Location_Type'] = [s.title() for s in mkip_data['Location_Type']]
mkvp_data.head(1)

# %%
mk_weapons_public = "https://query.data.world/s/tsuydmpezwzbjormbolhpi6eo34opd?dws=00000"
mkwp_data = pd.read_table(mk_incident_public, delimiter=",", header=0, skipinitialspace=True, engine="python", encoding="utf-8", encoding_errors="strict", on_bad_lines="warn")
mkwp_data.rename(str.title, axis="columns", inplace=True)
mkwp_data.rename({"Incident_Id":"Incident_ID","Firstcod":"FirstCOD", "Secondcod":"SecondCOD" }, axis="columns", inplace=True)
mkwp_data['FirstCOD'] = [s.title() for s in mkip_data['FirstCOD']]
mkwp_data['Location_Type'] = [s.title() for s in mkip_data['Location_Type']]
mkwp_data.head(1)

# %% [markdown]
# <code style="color: #b2c2bf;">@Credit: USA TODAY/AP/Northeastern University
# 
# About the data
# 
# The USA TODAY/AP/Northeastern University mass killing database contains information on incidents, offenders, victims and weapons for all multiple homicides with four or more victims killed in the United States from 2006 to the present.
# 
# Definition
# 
# A mass killing is defined as the intentional killing of four or more victims – excluding the deaths of unborn children and the offender(s) – by any means within a 24-hour period.
# 
# This definition includes cases involving all weapons (shooting, blunt force, stabbing, explosives), types (public, felony-related, and familicides), motivations (domestic dispute, profit, revenge, terrorism, hate), victim-offender relationships (stranger, family, acquaintance, co-worker), and number of locations. The time frame of 24 hours was chosen to eliminate conflation with spree killers who kill multiple victims over several days in different locations and to satisfy the traditional requirement of occurring in a “single incident,” even if that incident involves an offender targeting multiple locations in an extended assault but within a relatively short time span. However, offenders who kill four or more victims during any 24-hour period of time as part of a multi-day spree are included, as are all their victims within seven days of the mass killing. Negligent homicides related to driving under the influence or accidental fires are excluded because of the lack of intent. Finally, only incidents occurring within the 50 U.S. states and the District of Columbia are included in the database.
# 
# Consistent with the traditional definition, fatal mass shootings are mass killings (four or more victim fatalities) in which most or all the victims are killed by gunfire. This differs from an alternative definition used by the Gun Violence Archive that includes incidents in which at least four victims are shot regardless of whether the injury is fatal. Less than 5% of the mass shootings listed in the Gun Violence Archive are defined as mass killings in our database. Our definition of a fatal mass shooting also differs from an active shooter event which, as characterized by the FBI, involves an individual actively engaged in killing or attempting to kill people in a populated area. Less than 25% of active shooter events result in four or more victim fatalities, constituting a mass killing.
# 
# Methods
# 
# Researchers at USA TODAY first identified potential incidents using the FBI’s Supplementary Homicide Reports (SHR). Homicide incidents in the SHR were flagged as potential mass killing cases if four or more victims were reported on the same record, and the type of homicide was coded as “murder or non-negligent manslaughter.” Cases were subsequently verified utilizing media accounts, court documents, academic journal articles, books and local law enforcement records obtained through Freedom of Information Act (FOIA) requests. Each data point was corroborated by multiple sources, which were compiled into a single document to assess the quality of information. When sources were contradictory, official law enforcement or court records were used, when available, followed by the most recent media or academic source. Case information was subsequently compared with other available mass killing or mass shooting databases to ensure validity. Incidents listed in the SHR that could not be independently verified were excluded from the database.
# 
# In 2016, primary data collection and verification efforts shifted from USA TODAY to Northeastern University. Northeastern researchers conducted extensive searches for incidents not reported in the SHR during the time period, utilizing internet search engines including Lexis-Nexis, Google News, and Newspapers.com. Search terms included: [number] dead, [number] killed, [number] slain, [number] murdered, [number] homicide, mass murder, mass shooting, massacre, rampage, family killing, familicide and arson murder. Offender, victim and location names were also directly searched when available. Northeastern University researchers also independently verified data collected by USA TODAY staff and filled in missing information, sometimes involving updated reports on older cases.
# 
# In December 2018, a Memo of Understanding (MOU) was signed by The Associated Press, USA TODAY and Northeastern University to formalize a joint initiative to maintain and expand the mass killing database previously housed at USA TODAY. The Associated Press hosts the database and maintains the data entry tool, USA TODAY has developed and maintains the public website for and visualizations of the database, and Northeastern University manages data collection and updates.
# 
# The full database currently consists of four linked data tables with a total of 59 data fields (not counting indicators for the availability of offender/victim identity) –18 fields for each incident, 20 fields for each offender, 13 fields for each victim killed and eight fields for each weapon used. Most variables, with the notable exception of victim names, are available for public download. The remaining data is reserved for individuals affiliated with The Associated Press, USA TODAY/Gannett, and Northeastern University’s School of Criminology and Criminal Justice, and others by permission of all three organizations. Moving forward, additional variables may be added to the full database as well as the public subset. While USA TODAY respects diversity of gender, this database instead uses sex as a datapoint as is common in crime statistics.
# 
# 
# Any questions or corrections concerning the data should be directed to James Alan Fox at j.fox@northeastern.edu.
# 
# Credits
# 
# Research and reporting: Karina Zaiets and George Petras
# 
# Design and development: Veronica Bravo and Mitchell Thorson
# 
# Editing: Shawn J. Sullivan
# 
# Paul Overberg, Meghan Hoyer, Mark Hannan, Jodi Upton, Barbie Hansen, and Erin Durkin contributed to the original 2012 data reporting effort at USA TODAY.</code>


