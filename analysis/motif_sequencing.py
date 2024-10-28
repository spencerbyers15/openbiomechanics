"""
Pitchers have heirarchal goals that sometimes align and other times conflict with one another.

1. Throw with velocity using the least amount of effort
2. Give pitches unexpected shapes (using spin, arm slot, seams, etc.)
3. Create deception with delivery, making it difficult for batters to pick up the ball
4. General ability to locate pitches (conflicts with 1 and 2, potentially 3)
5. Minimize injury risk (conflicts with 1, potentially 2)
6. Get as many outs as possible (conflicts with 1 and 5)

Basically, their goal is to get batters out, and depending on their role get the most batters out they can while staying healthy. 
It is pretty clear from research and intution that the best way to get batters out is to throw the ball with high velocity,
therefore making the sensorimotor task of hitting the ball more difficult. Additionally, making the ball move in unexpected ways
based on the batter's expectations makes a pitch more difficult for a batter to hit. The synergy between pitch movement profiles
also can be beneficial for getting batters out, making their task of squarely hitting the ball more difficult, and potentially 
even making swing decisions more difficult. Finally, the ability to locate pitches around target locations is important for 
sequencing pitches together, and keeping batters from being able to shrink their decision space. 

In this project I have access to the open-source biomechanics dataset generously provided by Driveline's openbiomechanics project. 
This dataset contains kinematic and kinetic data for a variety of pitches thrown by pitchers across a variety of levels. 
Their previous work that has been provided with the datasets has calculated a number of metrics that are useful for understanding
how pitchers generate velocity (e.g. hip-shoulder separation, peak shoulder rotation velocity, etc.).

I'm interested in studying the sequences of movement motifs throughout a pitcher's delivery, and how reliable that sequence is across 
pitches intra-pitcher and inter-pitcher. Some keypoints in a delivery that can be binarized into point events and sequenced in time are:

(1) Knee lift to peak, (2) hands separation, (3) beginning of forward movement down mound, (4) arm cocking in backswing, (5) peak shoulder rotation,
(6) pelvis first rotating open, (7) front foot ground contact, (8) torso first rotating open, (9) full weight on front foot, (10) ball release (and more)

I'm interested in understanding how these point events are sequenced in time, and how that sequence is related to the pitch outcome.
"""

# LOAD DATA FROM SQL DB

