# -*- coding: utf-8 -*-
"""This module contains the classes to represent the provenance
of query results and explanations.
"""

class SchemaProvenance(object):
    """An object that holds basic logical provenance for group by aggregates
    
       Contains the following fields: 
            data (pd.DataFrame): The original dataframe,
            withfn (String): A Pandas aggreagte,
            groupby (List[String]): The list of group by columns,
            col (String): The aggregation column,
            hidden (List[String]): The columns aggregated out
    """

    def __init__(self, data, withfn, groupby, col):
        """Constructor

        data (pd.DataFrame): The original dataframe,
            withfn (String): A Pandas aggreagte,
            groupby (List[String]): The list of group by columns,
            col (String): The aggregation column,
            hidden (List[String]): The columns aggregated out

        """

        all_cols = list(data.columns.values)
        all_cols = self._removeall(all_cols, groupby)
        all_cols = self._removeall(all_cols, [col])

        self.data = data
        self.hidden = all_cols
        self.groupby = groupby
        self.col = col
        self.withfn = withfn

    def _removeall(self, l1, l2):
        return [l for l in l1 if not l in l2]
