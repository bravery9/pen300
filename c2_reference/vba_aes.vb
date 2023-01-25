Function Min(a, b)
    Min = a
    If b < a Then Min = b
End Function

Function B64Encode(bytes)
    Dim result As String
    Dim b64Block() As Byte
    Dim b64Enc As Object
    Dim utf8 As Object
    Dim Offset, Length, BlockSize As Integer
    
    Set b64Enc = CreateObject("System.Security.Cryptography.ToBase64Transform")
    Set utf8 = CreateObject("System.Text.UTF8Encoding")
    BlockSize = b64Enc.InputBlockSize
    For Offset = 0 To LenB(bytes) - 1 Step BlockSize
        Length = Min(BlockSize, UBound(bytes) - Offset)
        b64Block = b64Enc.TransformFinalBlock((bytes), Offset, Length)
        result = result & utf8.GetString((b64Block))
    Next
    B64Encode = result
End Function

Function B64Decode(b64Str)
    Dim utf8 As Object
    Dim bytes() As Byte
    Dim b64Dec As Object
    
    Set utf8 = CreateObject("System.Text.UTF8Encoding")
    Set b64Dec = CreateObject("System.Security.Cryptography.FromBase64Transform")
    bytes = utf8.GetBytes_4(b64Str)
    B64Decode = b64Dec.TransformFinalBlock((bytes), 0, UBound(bytes))
End Function