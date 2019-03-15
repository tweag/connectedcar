
# Connected Car Challenge

This text aims to briefly describe the analysis of the sample data designed for the _Connected Car Challenge_. You can obtain the data from [here](https://drive.google.com/file/d/1XIRQkLfjzRjmeDSB8zOmyuJn_C6R62ni/) and the webpage of the challenge [here](http://occ-challenge.strikingly.com/).


## Cleaning the data

As the first step towards the understanding the data we made it as something we can read and plot from. As a first try to look at the data, you would obtain something a bit mysterious: 

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>(1497925598.604522)</td>
      <td>can0</td>
      <td>233#2F0FFF0C00D10100</td>
    </tr>
    <tr>
      <th>1</th>
      <td>(1497925598.604710)</td>
      <td>can0</td>
      <td>223#890513004A000081</td>
    </tr>
    <tr>
      <th>2</th>
      <td>(1497925598.606356)</td>
      <td>can0</td>
      <td>00E#20E3200004FF40E2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>(1497925598.606391)</td>
      <td>can0</td>
      <td>228#40C040A1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>(1497925598.608609)</td>
      <td>can0</td>
      <td>408#20</td>
    </tr>
  </tbody>
</table>
</div>


As you can see the data is not meaningful yet. We guesssed that the first columns corresponds to the time steps the CAN recieve the data, . The third column corresponds to two parts, the one before `#` and the one after. The number (in hexadecimal base) before `#` is the id of the measurement (e.g. temperature, acceleration) and the other one corresponds to the value of the measurement. We seperated the data into different groups by using of the ids of measurements. We dropped then the ids that are (alsmot) constant. The total number of ids were 268 whilst there were 105 of them with significant information (variation).

We plotted all signals and obtained the following figure:

<img src="totalplotting.png"
     alt=" "
     style="float: center; margin-right: 10px;" />


There are a few things we have to notice here:

1. The signals do not start at the same time. Some of them are registered from time 0 while there are the ones which starts at 350 second later (in 10 minutes). The same story for the endings

2. Some of the signals are just a slight shift (in time) of each other.

3. There are a very highly oscilating signals. We should put a low-pass filter to take a better picture about their evolution.