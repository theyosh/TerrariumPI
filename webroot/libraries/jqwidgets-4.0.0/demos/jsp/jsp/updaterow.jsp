<%@ page import="java.lang.*"%>
<%@ page import="java.sql.*"%>
<%@ page import="com.google.gson.*"%>
<%
	String rowToUpdate = request.getParameter("id");
	String FirstName = request.getParameter("FirstName");
	String LastName = request.getParameter("LastName");
	String Title = request.getParameter("Title");
	String BirthDate = request.getParameter("BirthDate");

	//database connection
	// "jdbc:mysql://localhost:3306/northwind" - the database url of the form jdbc:subprotocol:subname
	// "root" - the database user on whose behalf the connection is being made
	// "abcd" - the user's password
	Connection dbConnection = DriverManager.getConnection(
			"jdbc:mysql://localhost:3306/northwind", "root", "abcd");

	// update specified record from the database
	Statement updateRecord = dbConnection.createStatement();
	int update = updateRecord
			.executeUpdate("UPDATE employees SET FirstName='"
					+ FirstName + "', LastName='" + LastName
					+ "', Title='" + Title + "', BirthDate='"
					+ BirthDate + "' WHERE EmployeeID=" + rowToUpdate);
%>