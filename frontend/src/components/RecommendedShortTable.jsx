import { useMemo } from 'react';
import { COLUMN_NAMES, getColumnAccessor, RecommendedTable, SENTIMENT, SentimentBackground } from './RecommendedTable';

/**
 * Component for Recommended Short Table on Home page. 
 */
const RecommendedShortTable = ({ data }) => {
  // Sorting by biggest changes (considering absolute value of the change regardless of positive or negative)
  console.log(data)
  data.sort((a, b) => {
    aAbs = Math.abs(parseFloat(a.sentiment));
    bAbs = Math.abs(parseFloat(b.sentiment));


    if (aAbs == bAbs) {
      // Sort by acsending company names to resolve ties
      if (a.company < b.company) return -1;
      else return 1;
    } else {
      if (bAbs > aAbs) return 1;
      else return -1;
    }
  });
  const columns = useMemo(
    () => {
      return (Object.entries(COLUMN_NAMES)).map(([header_key, header_value]) => ({
        accessorFn: (originalRow) => getColumnAccessor(originalRow, header_key),
        id: header_value,
        header: header_value,
        Header: <b style={{ color: 'black', fontSize: '0.9rem' }}>{header_value}</b>,
        Cell: ({ cell }) => {
          const isPositive = cell.getValue() > 0;
          const symbol = isPositive ? SENTIMENT.POSITIVE : SENTIMENT.NEGATIVE
          return header_value === "Sentiment" ?
            <SentimentBackground change={cell.getValue()} symbol={symbol} isPositive={isPositive} />
            : undefined
        }
      }))
    }
  )

  const props = { columns: columns, data: data, title: "The Biggest Sentiment Movers" }
  return <RecommendedTable {...props} />
}

export default RecommendedShortTable;