Calculator.py

Phase 1:

First, I setup the functions for the basic math functions.

# Math Functions
counts_per_360 = 360 / (0.022 * 1.0)
inches_per_360 = counts_per_360 / 1600
cm_per_360 = inches_per_360 * 2.54

count is the number that is detected by the OS from the mouse, 360 is  what it takes to do a full360 in game, 0.022 is the m_yaw value from CS2 and 1.0 is the in game sensitivity.

inches is setup to include the DPI in our case it is 1600, reason why we convert  to inches before cm is because DPI literally stands for Dots (Counts) Per Inch.

cm finally we convert the inches into cm, since that is the most common way to find your cm/360 value. 2.54 cm = 1 inch, that's why 2.54 cm is used.

Output for the first phase

Code: 
print(f"cm per 360: {cm_per_360:.2f}")

-print is the output command in python
-f-string is a function to make an output more specific
-"" is to turn our text into a string that will output
-.nf (.2f) this is a function that rounds the decimal of a value so you are not left with an extremely long and accurate number

Phase 2:

Making the code resuable instead of static to one game. 

The first step we created a function called sensitivity_to_cm360 with the parameters (sensitivity, yaw, dpi) and for our math functions we went in and indented everything to be inside of our new defined function. In addition we took our static numbers and replaced them with our functions parameters.

A parameters is a subset of a value range for an individual item, meaning that the item could have a different number because not everyone uses the same sens or dpi and every game does not share the same yaw value.

Second step we created a return value

typically you'll have the return value after your function especially if you're including some math invovled.  The two main components of a return statement is the result and the return.

 result = cm_per_360
 return result

Your result is the overarching outcome of your function and essientially you're telling python to return the result with a return statement.

A return function is needed because the function will do the math without telling you the actual result.

Third step was creating a statement that calls to the function to get tjh result printed and you need the statement in order to actually input the varied numbers we could put in.

Calculator.py

Phase 2

Reverse Function [cm360 to sens]

First thing we did was setup a function for calculating cm360 to sensitivity,

The reason why we want to do this in reverse is to make sure our math is correct.

(The reverse function takes a target cm/360 and a game's yaw and tells you what sensitivity to set in that game. This is what users actually need — they know their target feel, and they want the correct number to type into their game settings.)

for our function we did 

def cm360_to_sensitivity(cm360, yaw, dpi)

We used these definitions because we already know what cm360 is and we're solving for the sensitivity,

Now mostly the math is in the opposite direction, so for our first math function we will turn our cm into inches.

for our first math expresson we did

inches360 = cm360/2.54

by doing this we converted our cm into inches so that bring us to the next step which is figuring out the counts per inch

in order to figure out the counts per inch we needed to take the inches360 multiplied by our dpi (1600)

for this function it looked like 

counts360 = inches360 * dpi

lastly we need to solve for the sensitivity

for this expression we did 

sensitivity = 360 / (counts360 * yaw)

so just like in algebra we would solve what is in the parathensis first. our counts360 ended (by doing the math) being 16,368 and multiplying that by 0.022 we got 360.096 then we divide by 360 and end up with 1 
