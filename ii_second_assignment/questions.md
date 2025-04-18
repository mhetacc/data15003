# Usable Attributes

Attributes:
- Region
- ClassGrade
- Gender
- Ageyears 
  - *how old are they*
- Languages_spoken
- Travel_to_School 
  - *by car or bus or*
- Travel_time_to_School  
  - *commuting time*
- Reaction_time
- Score_in_memory_game
- Favourite_physical_activity
- Importance_reducing_pollution 
  - *[0, 1000]*
- Importance_recycling_rubbish
- Importance_conserving_water
- Importance_saving_energy
- Importance_owning_computer
- Importance_Internet_access
- Vegetarian
- Favorite_School_Subject
- Sleep_Hours_Schoolnight
- Sleep_Hours_Non_Schoolnight
- Communication_With_Friends  
  - *preferred type of communication*
- Text_Messages_Sent_Yesterday
- Text_Messages_Received_Yesterday
- *Hours of specific activity:*
    - Hanging_Out_With_Friends_Hours
    - Talking_On_Phone_Hours
    - Doing_Homework_Hours
    - Doing_Things_With_Family_Hours
    - Outdoor_Activities_Hours
    - Video_Games_Hours
    - Social_Websites_Hours
    - Texting_Messaging_Hours
    - Computer_Use_Hours
    - Watching_TV_Hours
    - Paid_Work_Hours
    - Work_At_Home_Hours
- Schoolwork_Pressure
- Planned_Education_Level
- Superpower
- Preferred_Status
  - *rich or happy or*
- Role_Model_Type
- Charity_Donation

### Some can be put together:
- median as **environmentalist_score:**
  - Importance_reducing_pollution 
  - *[0, 1000]*
  - Importance_recycling_rubbish
  - Importance_conserving_water
  - Importance_saving_energy
- median as **tech_oriented:**
  - Importance_owning_computer
  - Importance_Internet_access

**Observation:** *Importance of saving energy my be considered less common in tech oriented since ai/servers/etc?*

## Questions

### Grade Retention  
age + grade + gender 
Distribution among genders of grade retention, or starting earlier.

Maybe also + state.

### main transportation method + commuting time + [average USA car speed]
Shows how car centric USA is, how big it is + average distance of the students

### reaction time + short term memory + favourite sport
Can be used to see if there is some correlation 

#### + gender + age
Only with sport we can see if there is a preference, with all the rest we can try to look for correlations (or the absence of)

### vegetarian + gender + age + environmentalist
See if there are some correlations 

### favourite subjects + gender + age + vegetarian + environmentalist + tech oriented
See if there are some correlations

### hours of sleep (both) + gender + age + tech oriented 
Correlations?

### methods of communication + text in + text out + gender + age
Do male/female communicate differently and do they receive/send less/more text?

### activity hour estimation + gender + age + favourite subject + favourite sport + environmental + tech-oriented 
Look for correlations

### schoolwork pressure + timeof[homework, hanging out, sports, paid work, housework] + gender + age + highest level of education wanted
See some correlation between genders and "effort" or ambitions

### richOrHappy + gender + age + look up to + activity hour estimation + charity + highest level of eduction wanted
See if correlations between how they want to be, who they want to be, gender and ambitions

### bonus: gender + age + superpower
For fun

# Useless Attributes

All americans
- country


Too hard to use meaningfully
- year of survey 

Physical attributes are not interesting unless we want to talk about garments (e.g., if we wanted to produce school uniforms hence decide which sizes) or if we wanted to provide pens to all student
- right/left handed
- height
- foot length
- arm span
- left foot length
- longer foot
- length of fingers


some correlation? not likely or just unimportant information
- born in which month
- favorite season 
- allergies
- favorite food
- most drank type of beverage


can be an indicator of wealth but its too vague
- people live in your home


almost everyone has it
- internet access


not a lot of correlation with anything except gender or age
- favourite type of music


# Observations

## Grade Retention

- With full data we get a graph that is not particularly useful, since some data points are too far from the majority 
- With purged data things become more readable
- Second iteration (purged data) has some problems:
  - Stacked data make it seems like grade retentions increases over the years 
  - What if this is the result of a distribution of data i.e., we have more data points of ages between 16 and 18?
- Previous points are shown correct in the boxplot: median of grade retention stays the same throughout the years
- 1 or 2 years may not mean that student was held back or moved forward:
  - maybe just started earlier or later
  - we don't know when the survey was taken, so we cannot use month of birth to calculate if the year is correct but they just didn't have birthday yet   


While it would be interesting to add to this data geographical data (choropleth map of USA), this feels un-interesting because of how little variance there is, meaning we will likely go nowhere.

Surely one thing: no need to divide by gender since we have seen how little difference there is.

Added and as we surmised there is not a lot of difference. Coloring make it seem pretty dramatic while in reality the difference is between [-1, 2].