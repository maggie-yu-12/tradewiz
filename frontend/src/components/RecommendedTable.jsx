
import {
  Box,
  CircularProgress, Fade, Paper, TableContainer
} from '@mui/material';
import MaterialReactTable from 'material-react-table';

import { BsQuestionCircle } from 'react-icons/bs';
import { Popup } from 'semantic-ui-react';

// Enums

export const SENTIMENT = Object.freeze({
  POSITIVE: "▲",
  NEGATIVE: "▼",
});

export const COLUMN_NAMES = Object.freeze({
  COMPANY: "Company",
  WEEK: "1-Week Sentiment Score",
  MONTH: "1-Month Sentiment Score",
  SENTIMENT: "Sentiment",
  ACTIVITY: "Activity"
});

export const getColumnAccessor = (originalRow, key) => {
  switch (key) {
    case "COMPANY":
      return originalRow.company
    case "WEEK":
      return originalRow.week
    case "MONTH":
      return originalRow.month
    case "SENTIMENT":
      return originalRow.sentiment
    case "ACTIVITY":
      return originalRow.activity
  }
}

/**
 * Background for sentiment arrows: light green for positive, light red for negative
 */
export const SentimentBackground = ({ change, symbol, isPositive }) => (
  <>
    {/* <p style={{ display: "inline" }}> {isPositive ? "Positive" : "Negative"}</p> */}
    <Box
      sx={{
        backgroundColor:
          isPositive
            ? 'rgba(67, 157, 98, 0.5)' : 'rgba(241, 72, 110, 0.5)',
        borderRadius: '10px',
        color: isPositive
          ? 'rgba(67, 157, 98, 1)' : 'rgba(241, 72, 110, 1)',
        maxWidth: '5em', // setting the background box
        maxHeight: '2em',
        textAlign: 'center', // centering arrow symbol
        padding: '0',
        margin: '0'
      }}
    >
      <p style={{ fontSize: '0.9em', margin: '0', padding: '0' }}>{change + "% " + symbol}</p>
    </Box >
  </>
)

/**
 * Generic Recommended Table component in Home page
 */
export const RecommendedTable = ({ columns, data, title }) => {
  return (
    <>

      {data.length == 0 ? <CircularProgress /> :
        <Fade in={true} timeout={1000}>
          <div>
            <div className="header-container">
              <p id="table-header">{title}</p>
              <div id="question-popup">
                <Popup
                  content='This table is currently based on Tweets. 1-week sentiment score shows the averaged sentiment score of tweets about the company past 7 days, similarly for 1-moonth sentiment score. Sentiment shows the change in sentiment compared to the previous week. Activity shows the number of tweets past 24 hours.'
                  on='click'
                  pinned
                  trigger={<BsQuestionCircle />}

                />
              </div>
            </div>
            <TableContainer component={Paper} elevation={3} sx={{ maxHeight: '80vh', maxWidth: '80vw' }}>
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
                    fontSize: '1.1rem',
                  },
                }}
                muiTableBodyCellProps={{
                  sx: {
                    '&:hover': {
                      backgroundColor: '#ebebeb',
                    },
                    paddingLeft: '15px',
                    paddingRght: '10px',
                    paddingTop: '8px',
                    paddingBottom: '8px',
                    backgroundColor: 'white',
                    fontSize: '1rem',
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
          </div>
        </Fade>
      }
    </>
  )
}