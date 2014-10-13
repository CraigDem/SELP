# Project #


For my project, I propose a text-based game where users will create their own civilization and then compete with other civilizations in war, economics and politics. 

## Single Player ##

Civilizations will begin with two or three natural resources which provide stat bonuses and can trade these resources with other nations to create larger combined resources with additional stat bonuses. 

Civilizations would have five main mechanics they'd have to purchase. 

Firstly, "infrastructure" (working title) that would control how many citizens and other non-technological powers a civilization would have. 

Secondly, "technology" (working title) that would control how technologically advanced a nation would be, providing access to better military units such as aircraft, warships and eventually nuclear weapons. 

Thirdly, land that would control the size of the nation, and would be required to stop excessive population density leading to unhappyness.

Fourth, civilizations would be able to develop National Improvements which are structural improvements to the nation such as banks, stadiums, police/fire stations that offer larger stat bonuses for a larger cost. 

Finally, civilisations would also be able to develop National Wonders which are expensive, one-time purchase expensive developments such as a stock exchange which will offer huge stat bonuses at huge cost.

### Civilisation Statistics ###

The nation would have various stats which would alter things like tax income, bill expenditure and war time effectiveness. These would be altered by a wide range of game mechanics. A basic working implementation could involve things such as population happiness, density, literacy levels, type of government and other factors. I think this is definately an area where if I have extra time I could add more mechanics and increase the complexity or depth of the game dramatically.

## Multi-Player ##

Civilizations can join an alliance, similar to how for example a real country could join NATO, in the hope of organizing for war and trade. This would be visible in game and statistics of alliances could be viewed as well as statistics of individual nations, allowing competitiveness on both a single player and multi-player level. 

Civilizations would be able to send/receive money, a technological resource, and soldiers amongst allies. This gives a boost for well organised groups and encourages player interactivity.

## Scoring Mechanic ##

Nations can be ranked on several factors. For example: land, "infrastructure", "technology", numbers of National Improvements and National Wonders, army size, population size and others. Since these will all be stored in the same database of a nation, it should be a trivial task to display rankings.

# Technical Remarks #

## Time Passing ##

This is a text based game, and tasks will need to be time limited. I plan to have tax income be collectable once a day and bills able to be paid once a day as well. However, to add stratagy and encourage activity, I think tax and bills should occur interest every day they are not collected or paid. This means that an interesting stratagy of a nation paing bills daily but collecting taxes less frequently could lead to player's being able to stratagise and optimize their economies. There will need to be a limit to how long taxes/bills can be left without being paid. I plan to cap taxes at 20 days and no extra interest will be generated after that time. I also plan to have nations be deleted for inactivty after 30 days of taxes not being paid. This I think would cut down on unnessecary database size and keep the player base active.

I would have bills become 'due' after two days unpaid and then bills would need to be paid before any major purchasing of game mechanics could continue. 

There would also be various game mechanics that are on a timer. For example, wonders might only be purchaseable monthly or weekly. Nuclear weapons might only be able to be developed once a day. There could be other wonders that shorten these "cooldowns" if I have time to implement them. Basic implementation would have all game mechanics with their own cooldowns but not have any way to decrease them. 

Nations would be able to perform a set a maximum amount of waring actions per day as well, for example deploying military and actually staging offensives.

This of course leads to the idea of an "update". Where the game refreshes day-on-day and things become purchaseable again. I think this should be midnight to co-incide with the idea of a day. But in practice, playing habits could mean that having an update earlier could lead to more players being able to be online at that time and make stategic plays (for example attacking a nation right before update and then right afterwards when the cooldowns reset) more viable.

## Backend ##

I intend to use python with the django framework for the computational backend. Being a text based game, I believe the most demanding part of the process will be on page load when a nation's information will be loaded from the database and any required computations performed before the results are passed to the frontend. It could be possible to do certain tasks asyncorniously but I'm unsure if there would be in any benifits in this situation. It could aid immersion and UI cohesiveness to have as few page loads as possible however. I think I'll test both and see if there is a notable difference.

## Database ##

Since this is a text based game, basically every page load will draw information from the database. For my database, I have chosen to use mySQL. This is supported very well by django and I don't forsee any issues with using it. I have chosen this over SQLite because at times where the server will update (i.e move to the next day and reset purchase/war timers) there may be a peak of players and concurrency required. This may be slight overkill on a small-scale project but in a production environment I think this is the best choice, and I'm going to treat this project as if it was going to be in a large production environment.


For the frontend, I intend to use the bootstrap framework to easily create a unified UI using HTML, CSS and Javascript. I believe bootstrap offers a cohesive UI with the least amount of difficulty while still allowing for huge extensibility.

# Time Requirements #

I've been allocated 95 hours for this project, and I think this project is definately deliverable within that timeframe.

I believe the frontend will not take me a lot of time, I've used HTML/CSS/JS and specifically the bootstrap framework extensively before. But I've moved away from PHP to Python/Django for this project and there will be a learning curve attached to that. In return I hope that with Django's more modern approach to web development (e.g virtualisation), it will be worth it. It will also be far easier to run a webserver for Django as opposed to a full LAMP (Or nginx) stack. 

Therefore, I plan to have the breakdown of hours be something like this:

<table style="width:100%">
  <th>
    <td>Task</td>
    <td>Hours</td> 
  </th>
  <tr>
    <td>Research</td>
    <td>3</td> 
  </tr>
  <tr>
    <td>Proposal</td>
    <td>2</td> 
  </tr>
  <tr>
    <td>Design</td>
    <td>5</td> 
  </tr>
  <tr>
    <td>Environement Setup</td>
    <td>5</td> 
  </tr>
  <tr>
    <td>Learning Django</td>
    <td>5</td> 
  </tr>
  <tr>
    <td>Implementation</td>
    <td>65</td> 
  </tr>
  <tr>
    <td>Testing</td>
    <td>5</td> 
  </tr>
  <tr>
    <td>Reflection and Reporting</td>
    <td>5</td> 
  </tr>

</table>
 