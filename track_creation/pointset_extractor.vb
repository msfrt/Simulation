Option Strict Off
Imports System
Imports System.IO
Imports NXOpen
Imports NXOpen.Features
Imports NXOpen.UF
 
Module PointDataToFile
    Dim s As Session = Session.GetSession()
    Dim ui As UI = UI.GetUI()
    Dim ufs As UFSession = UFSession.GetUFSession()
    Dim wp As Part = s.Parts.Work
    Sub Main()
        'set up code to get the nx session and defines the variables
        ' select point set feature
        Dim feat As Feature = Nothing
        Dim pointSet1 As PointSet = Nothing
        Dim thePoints(-1) As Point
        Dim response1 As Selection.Response = select_feature(feat)
        If feat.GetFeatureName.ToString.Contains("Point Set") Then
            pointSet1 = DirectCast(feat, PointSet)
            thePoints = pointSet1.GetPoints
        Else
            Exit Sub
        End If
 
        'Open file to write contents.
        Dim objStreamWriter As StreamWriter 'defines method to write to file
 
        'Specify directory to write file to.
        objStreamWriter = New StreamWriter("C:\Users\nic\Documents\GitHub\Simulation\track_creation\temp.txt") 'creates the file and writes to this directory
 
        'Write file header.
        'Dim Header As String = “XYZ Coordinates of Points Defining Curve”
        'objStreamWriter.WriteLine(Header)
 
 
        'Define cnt1 (counter) to start at 1.
        'Dim cnt1 As Integer = 1
 
        'Write the xyz header line before the loop starts.
        'objStreamWriter.WriteLine(“Point, X, Y, Z”)
		
		'Write some headers just for some file context
        objStreamWriter.WriteLine(“This is a temporary file used in GPS track creation.”)
		objStreamWriter.WriteLine(“After you run the Python script to reformat the data,”)
		objStreamWriter.WriteLine(“you may delete this file.”)
		objStreamWriter.WriteLine(“”)
		
 
        'Loop.
        For Each pt As Point In thePoints
            'write contents of header2 and the counter to file
            'objStreamWriter.WriteLine(header2 & cnt1.ToString)
 
            'Write the xyz coordinates of points to the text file.
            objStreamWriter.WriteLine(Math.Round(pt.Coordinates.X, 3).ToString & “ ” & Math.Round(pt.Coordinates.Y, 3).ToString & “ ” & Math.Round(pt.Coordinates.Z, 3).ToString)
 
            'Start the counter.
            'cnt1 += 1 ' same as saying cnt1 = cnt1 + 1
 
        Next
        'Close the file.
        objStreamWriter.Close()
    End Sub
    Public Function select_feature(ByRef feat As Feature) As Selection.Response
        Dim selobj As NXObject = Nothing
        Dim cursor As Point3d
        Dim typeArray() As Selection.SelectionType =
         {Selection.SelectionType.Features}
 
        Dim resp As Selection.Response = UI.SelectionManager.SelectTaggedObject("Select feature",
           "Select feature", Selection.SelectionScope.WorkPart, False, typeArray, selobj, cursor)
        If ((resp = Selection.Response.ObjectSelected) _
                    OrElse (resp = Selection.Response.ObjectSelectedByName)) Then
            feat = CType(selobj, Feature)
            Return Selection.Response.Ok
        Else
            Return Selection.Response.Cancel
        End If
    End Function
End Module