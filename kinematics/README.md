
# LTS Kinematic Curves

Unfortunately, Optimum K isn't very user friendly. Especially when trying to work with softwares outside of the Optimum G Suite (thanks, Claude). So, there are no scripts to automatically do the grunt work for us. We have to do manual calculations and enter in the values one-by-one into LTS, just like the good ol' days.


---

### Here's what you need to do:


1. LTS maps all of the suspension curves in terms of suspension displacement, which is great because OptK doesn't give you those. We will need to calculate it. Usually it's easiest to do the following calculations in an excel doc and then copy and paste everything into OptK. For suspension displacement, you're going to want to get the step motion ratio steps and coilover steps from OptK, and then you will perform the following calculation in excel to get suspension displacement:
  * coilover displacement * motion ratio
2. Now that you have susp. displacement, you can enter almost every curve into LTS. It's easiest to make the charts of the steps in excel, then copy and paste both columns into LTS at once. This saves you from having to manually enter susp. displacement 1,000 times.
