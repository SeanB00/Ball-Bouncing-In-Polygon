This is a simple simulation of a ball boncing in the a polygon.
The simulation runs at 60 FPS and uses relfection by flipping the norm factor (fourier term).
The formula for the reflected velocity (rv) over the reflected surface (s) is produced by:  
  v = <v, s>*s + <v,norm>*norm
  
  rv = <v, s>*s  - <v,norm>*norm  (the factor is reflected)
  
  => v + rv = 2 * <v,s>*s => rv = 2<v,s>s - v //
  
As for handling the collisions, I have used simple ray-casting to decide if a point is inside the polygon.
Then, I used sample points around the ball (plus a small gap I have added so the collisions will look cleaner) to know if the ball itself is inside the polygon.
For the graphics, I used pygame.
