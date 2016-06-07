<%@ page import="java.lang.*"%>
<%@ page import="java.sql.*"%>
<%@ page import="com.google.gson.*"%>
<%
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

	// delete specified record from the database
	Statement addToDb = dbConnection.createStatement();
	int add = addToDb
			.executeUpdate("INSERT INTO employees (FirstName, LastName, Title, BirthDate) VALUES ('"
					+ FirstName
					+ "', '"
					+ LastName
					+ "', '"
					+ Title
					+ "', '" + BirthDate + "')");
%>