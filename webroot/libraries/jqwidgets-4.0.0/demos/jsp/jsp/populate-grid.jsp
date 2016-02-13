<%@ page import="java.lang.*"%>
<%@ page import="java.sql.*"%>
<%@ page import="com.google.gson.*"%>
<%
	String where = "";

	String filterscount = request.getParameter("filterscount");

	if (Integer.parseInt(filterscount) > 0) {
		where = request.getParameter("where");
	}

	String sort = request.getParameter("$orderby");
	String pagenum = request.getParameter("pagenum");
	String pagesize = request.getParameter("pagesize");
	String start = "" + Integer.parseInt(pagenum)
			* Integer.parseInt(pagesize);

	// database connection
	// "jdbc:mysql://localhost:3306/northwind" - the database url of the form jdbc:subprotocol:subname
	// "root" - the database user on whose behalf the connection is being made
	// "abcd" - the user's password
	Connection dbConnection = DriverManager.getConnection(
			"jdbc:mysql://localhost:3306/northwind", "root", "abcd");

	// retrieve necessary records from database
	Statement getFromDb = dbConnection.createStatement();

	ResultSet totalEmployees = getFromDb
			.executeQuery("SELECT COUNT(*) AS Count FROM employees"
					+ where);

	String totalRecords = "";

	while (totalEmployees.next()) {
		totalRecords = totalEmployees.getString("Count");
	}
	totalEmployees.close();

	ResultSet employees = getFromDb
			.executeQuery("SELECT EmployeeID, FirstName, LastName, Title, BirthDate FROM employees"
					+ where
					+ " ORDER BY "
					+ sort
					+ " LIMIT "
					+ start
					+ ", " + pagesize);

	boolean totalRecordsAdded = false;

	// format returned ResultSet as a JSON array
	JsonArray recordsArray = new JsonArray();
	while (employees.next()) {
		JsonObject currentRecord = new JsonObject();
		currentRecord.add("EmployeeID",
				new JsonPrimitive(employees.getString("EmployeeId")));
		currentRecord.add("FirstName",
				new JsonPrimitive(employees.getString("FirstName")));
		currentRecord.add("LastName",
				new JsonPrimitive(employees.getString("LastName")));
		currentRecord.add("Title",
				new JsonPrimitive(employees.getString("Title")));
		currentRecord.add("BirthDate",
				new JsonPrimitive(employees.getString("BirthDate")));

		if (totalRecordsAdded == false) {
			// add the number of filtered records to the first record for client-side use
			currentRecord.add("totalRecords", new JsonPrimitive(
					totalRecords));
			totalRecordsAdded = true;
		}

		recordsArray.add(currentRecord);
	}
	out.print(recordsArray);
	out.flush();
%>