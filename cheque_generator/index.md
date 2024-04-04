# Rey's Sample Works - Cheque Generator

<a href="https://reytorremis.github.io/rey_sample_works/"><img src="https://img.shields.io/badge/HOME-GitHub" /></a>

## Description
A simple cheque writer coded in excel. The file uses Macros.

## Download Files

[Cheque Writer](final_version_cheque_writer-3_updated_02122024.xlsm)

### VBA Code

A function that spells a number, i.e. 9256 = Nine Thounsand Two Hundred Fifty Six
```
Function SpellNumber(ByVal numIn)
    Dim LSide, RSide, Temp, DecPlace, Count, oNum
    oNum = numIn
    ReDim Place(9) As String
    Place(2) = " Thousand "
    Place(3) = " Million "
    Place(4) = " Billion "
    Place(5) = " Trillion "
    numIn = Trim(Str(numIn)) 'String representation of amount
    ' Edit 2.(0)/Internationalisation
    ' Don't change point sign here as the above assignment preserves the point!
    DecPlace = InStr(numIn, ".") 'Pos of dec place 0 if none
    If DecPlace > 0 Then 'Convert Right & set numIn
        RSide = GetTens(Left(Mid(numIn, DecPlace + 1) & "00", 2))
        numIn = Trim(Left(numIn, DecPlace - 1))
    End If
    RSide = numIn
    Count = 1
    Do While numIn <> ""
        Temp = GetHundreds(Right(numIn, 3))
        If Temp <> "" Then LSide = Temp & Place(Count) & LSide
        If Len(numIn) > 3 Then
            numIn = Left(numIn, Len(numIn) - 3)
        Else
            numIn = ""
        End If
        Count = Count + 1
    Loop

    SpellNumber = LSide
    If InStr(oNum, Application.DecimalSeparator) > 0 Then    ' << Edit 2.(1)
        SpellNumber = SpellNumber & " and " & fractionWords(oNum) & " centavos"
    End If

End Function

Function GetHundreds(ByVal numIn) 'Converts a number from 100-999 into text
    Dim w As String
    If Val(numIn) = 0 Then Exit Function
    numIn = Right("000" & numIn, 3)
    If Mid(numIn, 1, 1) <> "0" Then 'Convert hundreds place
        w = GetDigit(Mid(numIn, 1, 1)) & " Hundred "
    End If
    If Mid(numIn, 2, 1) <> "0" Then 'Convert tens and ones place
        w = w & GetTens(Mid(numIn, 2))
    Else
        w = w & GetDigit(Mid(numIn, 3))
    End If
    GetHundreds = w
End Function

Function GetTens(TensText)  'Converts a number from 10 to 99 into text
    Dim w As String
    w = ""           'Null out the temporary function value
    If Val(Left(TensText, 1)) = 1 Then   'If value between 10-19
        Select Case Val(TensText)
            Case 10: w = "Ten"
            Case 11: w = "Eleven"
            Case 12: w = "Twelve"
            Case 13: w = "Thirteen"
            Case 14: w = "Fourteen"
            Case 15: w = "Fifteen"
            Case 16: w = "Sixteen"
            Case 17: w = "Seventeen"
            Case 18: w = "Eighteen"
            Case 19: w = "Nineteen"
            Case Else
        End Select
    Else      'If value between 20-99..
        Select Case Val(Left(TensText, 1))
            Case 2: w = "Twenty "
            Case 3: w = "Thirty "
            Case 4: w = "Forty "
            Case 5: w = "Fifty "
            Case 6: w = "Sixty "
            Case 7: w = "Seventy "
            Case 8: w = "Eighty "
            Case 9: w = "Ninety "
            Case Else
        End Select
        w = w & GetDigit _
            (Right(TensText, 1))  'Retrieve ones place
    End If
    GetTens = w
End Function

Function GetDigit(Digit) 'Converts a number from 1 to 9 into text
    Select Case Val(Digit)
        Case 1: GetDigit = "One"
        Case 2: GetDigit = "Two"
        Case 3: GetDigit = "Three"
        Case 4: GetDigit = "Four"
        Case 5: GetDigit = "Five"
        Case 6: GetDigit = "Six"
        Case 7: GetDigit = "Seven"
        Case 8: GetDigit = "Eight"
        Case 9: GetDigit = "Nine"
        Case Else: GetDigit = ""
    End Select
End Function

Function fractionWords(n) As String
    Dim fraction As String, x As Long
    fraction = Split(n, Application.DecimalSeparator)(1)   ' << Edit 2.(2)
    For x = 1 To Len(fraction)
        If fractionWords <> "" Then fractionWords = fractionWords & " "
        fractionWords = fractionWords & GetDigit(Mid(fraction, x, 1))
    Next x
End Function
```

