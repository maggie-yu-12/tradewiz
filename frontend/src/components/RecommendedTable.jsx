
import {
  Box,
  CircularProgress, Fade, Paper, TableContainer
} from '@mui/material';
import MaterialReactTable from 'material-react-table';

// Enums

export const SENTIMENT = Object.freeze({
  POSITIVE: "▲",
  NEGATIVE: "▼",
});

export const COLUMN_NAMES = Object.freeze({
  COMPANY: "Company",
  WEEK: "Week",
  MONTH: "Month",
  SENTIMENT: "Sentiment"
});

/**
 * Background for sentiment arrows: light green for positive, light red for negative
 */
export const SentimentBackground = ({ isPositive }) => (
  <Box
    sx={{
      backgroundColor:
        isPositive
          ? 'rgba(67, 157, 98, 0.5)' : 'rgba(241, 72, 110, 0.5)',
      borderRadius: '10px',
      color: isPositive
        ? 'rgba(67, 157, 98, 1)' : 'rgba(241, 72, 110, 1)',
      maxWidth: '2em', // setting the background box
      maxHeight: '2em',
      textAlign: 'center', // centering arrow symbol
      padding: '0',
      margin: '0'
    }}
  >
    <p style={{ fontSize: '0.9em', margin: '0', padding: '0' }}>{isPositive ? SENTIMENT.POSITIVE : SENTIMENT.NEGATIVE}</p>
  </Box >
)

/**
 * Generic Recommended Table component in Home page
 */
export const RecommendedTable = ({ columns, data }) => {
  return (
    <>
      {data.length == 0 ? <CircularProgress /> :
        <Fade in={true} timeout={1000}>
          <TableContainer component={Paper} elevation={3} sx={{ maxHeight: '50vh', maxWidth: '50vw' }}>
            <MaterialReactTable
              columns={columns}
              data={data}
              muiTableProps={{
                sx: {
                  tableLayout: 'fixed',
                },
              }}
              defaultColumn={{
                minSize: 20, //allow columns to get smaller than default
                maxSize: 9001, //allow columns to get larger than default
                display: 'inline-flex',
                size: 'min-content'
              }}
              muiTableHeadCellProps={{
                sx: {
                  paddingLeft: '1rem',
                  paddingRight: '1rem',
                  margin: 'auto',
                  backgroundColor: 'white',
                  textAlign: 'center',
                },
              }}
              muiTableBodyCellProps={{
                sx: {
                  '&:hover': {
                    backgroundColor: '#ebebeb',
                  },
                  paddingLeft: '15px',
                  paddingRght: '10px',
                  paddingTop: '5px',
                  paddingBottom: '5px',
                  backgroundColor: 'white',
                  fontSize: '0.9rem',
                },
              }}
              // enableRowSelection //enable some features
              enableRowNumbers
              // enableRowActions
              muiSearchTextFieldProps={{
                placeholder: 'Search Stock',
                sx: { minWidth: '18rem' },
                variant: 'outlined',
              }}
            />
          </TableContainer>
        </Fade>
      }
    </>
  )
}