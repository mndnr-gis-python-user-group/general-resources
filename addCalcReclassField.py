#-------------------------------------------------------------------------------
# Name:        addCalcRelcassField
# Purpose:     Adds a field, calculates field from crosswalk table. Check that
#              your crosswalk table joins to your join field in the feature
#              class without error prior to running. Parameters for adding the
#              script to an ArcToolbox are commented after the sys.argv
#              statements. Both the crosswalk table and the feature class must
#              be in a geodatabase. Field to be added is type "TEXT" and length
#              50. Modify in first Geoprocessing Task if needed. Take care to
#              use the same type for the Field to Add (fcNewField) and the
#              field that is used to calculate from (cwCalcField).
#
# Author:      jereinha
#
# Created:     05/09/2014
#-------------------------------------------------------------------------------

import arcpy, sys

def main():
    ##-------------------------- Input Parameters ----------------------------##
    fc = sys.argv[1]
    # Display Name: Input Feature Class
    # Data Type: Feature Class
    fcJoin = sys.argv[2]
    # Display Name: Input Feature Class Join Field
    # Data Type: Field
    # Obtained From: Input_Feature_Class
    fcNewField = sys.argv[3]
    # Display Name: Field to Add to Feature Class and Calculate
    # Data Type: String
    cw = sys.argv[4]
    # Display Name: Input Crosswalk Table
    # Data Type: Table
    cwJoin = sys.argv[5]
    # Display Name: Crosswalk Table Join Field
    # Data Type: Field
    # Obtained From: Input_Crosswalk_Table
    cwCalc = sys.argv[6]
    # Display Name: Crosswalk Table Calc Field
    # Data Type: Field
    # Obtained From: Input_Crosswalk_Table

    ##--------------------------- Geoprocessing ------------------------------##
    # Add field
    arcpy.AddField_management(fc, fcNewField, "TEXT", "", "", 50)

    # Search cursor on the input crosswalk table to control update of feature
    # class
    with arcpy.da.SearchCursor(cw, (cwJoin, cwCalc)) as rowsCw:
        # For each row in the cw table, update all like values in the added
        # field in the feature class
        for rowCw in rowsCw:
            # get value from join field of crosswalk table for whereclause value
            whereValue = rowCw[0]
            # check type for formatting in where clause
            varType = str(type(whereValue))
            # format where clause based on type
            if varType == "<type 'int'>" or\
               varType == "<type 'float'>":
                whereClause = "\""+fcJoin+"\" = "+str(whereValue)
            if varType == "<type 'unicode'>":
                whereClause = "\""+fcJoin+"\" = '"+str(whereValue)+"'"
            # show resulting clause for verification and progress
            arcpy.AddMessage("Calculating for: "+whereClause)
            # get value to set to from crosswalk table calc field
            rowValue = rowCw[1]
            # Update cursor on feature class for where clause and calc value
            # from row in crosswalk table
            counter = 0
            with arcpy.da.UpdateCursor(fc, (fcNewField), whereClause) as rowsFc:
                # Update added field in feature class to calc field in crosswalk
                for rowFc in rowsFc:
                    rowFc[0] = rowValue
                    rowsFc.updateRow(rowFc)
                    counter += 1
            arcpy.AddMessage("Count of records calculated: "+str(counter))

if __name__ == '__main__':
    main()