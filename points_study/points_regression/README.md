
# Event Time vs. Points Regression Generator

So, it turns out that Excel makes nice trend lines that *look* really accurate. However, when you display the equation from the line, and try to use it to predict function values, it's actually wildly wrong in many cases. It because of the necessary rounding when Excel displays points on a scatter plot's axis. There's probably a workaround somewhere, but upon a few google searches, I couldn't find anything newer than 2007, so I wrote a script! This script will generate predictions for resultant points as a function of event time.

---

### Here's what you need to do:

1. Change `f_in_path` on line 2 to the path of your points study Excel document (`.xlsm` extension - macros enabled, otherwise you wouldn't need to be using this scipt!).
2. You don't really need to change `f_out` on line 5. This is the output file name. By default, it saves in the running directory of the script, unless you provide a file path like on line 2.
3. Unless you've changed the tab names in your Excel doc, you won't need to change `tabs` on line 9.
4. You will most likely have to change `table ranges` on line 10. These ranges point to the columns and rows that store the time and points values that you would like the regression to be made from. Be sure to not include times that are in red, or points that have been awarded away from a trend-line. For example, don't include a team that DNF'd endurance but was still awarded 3 points for those 3 lonely laps that they completed.
5. The `poly_degree` parameter is used to store the degree of polynomial to be generated. A second degree polynomial (^2) provides a good enough regression in my oppinion. Once you up that number to 3 or higher, MATLAB might warn you that the polynomial is poorly conditioned, and that those regressions could be a little wonky.
6. Once you have your regressions, you can sauce them into the excel macros module. In your macro enabled Excel doc, press `Alt + f11` to bring up the macro editor. If no modules exist in the VBAProject file explorer on the left side, got to *Insert* and click *Module*. An example of a macro function is included below for your reference.

```vbscript
Function endurance_points(t)

    endurance_points = 0.000281 * t ^ 2 - 1.305057 * t + 1475.89843

    If endurance_points > 275 Then
        endurance_points = 275
    End If

End Function
```
