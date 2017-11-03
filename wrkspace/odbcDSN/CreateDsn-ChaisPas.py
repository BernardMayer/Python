# http://hex-dump.blogspot.fr/2005/05/creating-odbc-data-source-using-python.html
"""
 Creating an ODBC data source using Python
For the cross-platform installer I am creating, I need to create ODBC data sources for Windows installations. Thanks to the Python ctypes module the solution was as simple as:
"""

import ctypes

ODBC_ADD_DSN = 1        # Add data source
ODBC_CONFIG_DSN = 2     # Configure (edit) data source
ODBC_REMOVE_DSN = 3     # Remove data source
ODBC_ADD_SYS_DSN = 4    # add a system DSN
ODBC_CONFIG_SYS_DSN = 5 # Configure a system DSN
ODBC_REMOVE_SYS_DSN = 6 # remove a system DSN

def create_sys_dsn(driver, **kw):
    """Create a  system DSN
    Parameters:
        driver - ODBC driver name
        kw - Driver attributes
    Returns:
        0 - DSN not created
        1 - DSN created
    """
    nul = chr(0)
    attributes = []
    for attr in kw.keys():
        attributes.append("%s=%s" % (attr, kw[attr]))
    
    return ctypes.windll.ODBCCP32.SQLConfigDataSource(0, ODBC_ADD_SYS_DSN, driver, nul.join(attributes))

if __name__ == "__main__":
    print create_sys_dsn("SQL Server",SERVER="(local)", DESCRIPTION="SQL Server DSN", DSN="SQL SERVER DSN", Database="mydatabase", Trusted_Connection="Yes")
    #print create_sys_dsn("mySQL",SERVER="local", DESCRIPTION="mySQL Server Test1", DSN="mySQL DSN", DATABASE="mySQLDb", UID="username", PASSWORD="password", PORT="3306", OPTION="3")

