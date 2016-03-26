CREATE TABLE [dbo].[Employee] (
    [EmployeeID]      INT           IDENTITY (1, 1) NOT NULL,
    [ManagerID]      INT NULL,
    [FirstName]      NVARCHAR (50) NULL,
    [LastName]       NVARCHAR (50) NULL,
    [Title]       NVARCHAR (50) NULL,
    [Country]       NVARCHAR (50) NULL,
    [City]       NVARCHAR (50) NULL,
    [Address]       NVARCHAR (50) NULL,
    [HireDate]       DATETIME NULL,
    [BirthDate]       DATETIME NULL,
    PRIMARY KEY CLUSTERED ([EmployeeID] ASC)
);