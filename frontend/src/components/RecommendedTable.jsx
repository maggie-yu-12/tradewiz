import { useMemo } from 'react';

import {
  Box,
  CircularProgress, Fade, Paper, TableContainer
} from '@mui/material';
import MaterialReactTable from 'material-react-table';

export const RecommendedLongTable = ({ data }) => {
  const column_headers = useMemo(() => ["company", "symbol", "week", "month", "sentiment"])
  const Sentiment = Object.freeze({
    POSITIVE: Symbol("positive"),
    NEGATIVE: Symbol("negative"),
  });

  // {
  //   accessorKey: 'company', //simple recommended way to define a column
  //   header: 'Company',
  //   muiTableHeadCellProps: { sx: { color: 'blue' } }, //custom props
  // },
  const columns = useMemo(
    () => column_headers.map((header) => ({
      accessorFn: (originalRow) => getColumnAccessor(originalRow, header),
      id: header,
      header: header,
      Header: <i style={{ color: 'blue' }}>{header}</i>,
      Cell: ({ cell }) => header === "sentiment" ? (
        <Box
          sx={(theme) => ({
            backgroundColor:
              cell.getValue() === Sentiment.POSITIVE.description
                ? theme.palette.success.dark :
                theme.palette.warning.dark,
            borderRadius: '0.25rem',
            color: '#fff',
            textAlign: 'center',
            maxWidth: '50%',
            p: '0.25rem',
          })}
        >
          {cell.getValue()}
        </Box>
      ) : undefined
    }))
  )

  const getColumnAccessor = (originalRow, header) => {
    switch (header) {
      case "company":
        return originalRow.company
      case "symbol":
        return originalRow.symbol
      case "week":
        return originalRow.week
      case "month":
        return originalRow.month
      case "sentiment":
        return originalRow.sentiment
    }
  }

  const props = { columns: columns, data: data }
  return <RecommendedTable {...props} />
}

const RecommendedTable = ({ columns, data }) => {
  return (
    <>
      {data.length == 0 ? <CircularProgress /> :
        <Fade in={true} timeout={1000}>
          <TableContainer component={Paper} sx={{ maxHeight: "50vh", maxWidth: "80vw" }}>
            <div className='home-container'>
              <MaterialReactTable
                style={{ width: 100 }}
                columns={columns}
                data={data}
                // enableRowSelection //enable some features
                enableColumnOrdering
                enableGlobalFilter={false} //turn off a feature
                enableRowNumbers
                enableRowActions
                muiSearchTextFieldProps={{
                  placeholder: 'Search Stock',
                  sx: { minWidth: '18rem' },
                  variant: 'outlined',
                }}
              />
            </div>
          </TableContainer>
        </Fade>
      }
    </>
  )
}