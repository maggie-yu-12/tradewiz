import { useMemo } from 'react'
import { COLUMN_NAMES, RecommendedTable, SentimentBackground } from './RecommendedTable'

/**
 * Component for Recommended Short Table on Home page. 
 */
const RecommendedShortTable = ({ data }) => {
  const columns = useMemo(
    () => {
      return (Object.entries(COLUMN_NAMES)).map(([header_key, header_value]) => ({
        accessorFn: (originalRow) => getColumnAccessor(originalRow, header_key),
        id: header_value,
        header: header_value,
        Header: <b style={{ color: 'black', fontSize: '0.9rem' }}>{header_value}</b>,
        Cell: ({ cell }) => {
          const isPositive = cell.getValue() === 'positive'
          return header_value === "Sentiment" ?
            <SentimentBackground isPositive={isPositive} />
            : undefined
        }
      }))
    }
  )

  const getColumnAccessor = (originalRow, key) => {
    switch (key) {
      case "COMPANY":
        return (originalRow.company).concat(" (", originalRow.symbol, ")")
      case "WEEK":
        return originalRow.week
      case "MONTH":
        return originalRow.month
      case "SENTIMENT":
        return originalRow.sentiment
    }
  }

  const props = { columns: columns, data: data }
  return <RecommendedTable {...props} />
}

export default RecommendedShortTable;