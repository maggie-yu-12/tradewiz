import { useMemo } from 'react';
import { Link } from 'react-router-dom';
import { COLUMN_NAMES, getColumnAccessor, SENTIMENT, SentimentBackground, SentimentTable } from './SentimentTable';

/**
 * Component for Recommended Short Table on Home page. 
 */
const BiggestSentimentMoversTable = ({ data }) => {
  // Sorting by biggest changes (considering absolute value of the change regardless of positive or negative)
  data.sort((a, b) => {
    aAbs = Math.abs(parseFloat(a.sentiment.change));
    bAbs = Math.abs(parseFloat(b.sentiment.change));

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
        accessorKey: getColumnAccessor(header_key),
        id: header_value,
        Header: <b id="big-table-header" style={{ color: 'black', fontSize: '1.05rem', wordBreak: 'normal', whiteSpace: 'normal' }}>{header_value}</b>,
        Cell: ({ cell }) => {
          if (header_value === "Δ in Sentiment by Week") {
            const res_obj = cell.getValue()
            console.log(res_obj)
            const isPositive = res_obj.change > 0;
            const symbol = isPositive ? SENTIMENT.POSITIVE : SENTIMENT.NEGATIVE
            return (
              <SentimentBackground change={res_obj.change} symbol={symbol} isPositive={isPositive} prev={res_obj.prev} />);
          } else if (header_value === "Company") {
            path = "/stockdata?symbol=" + cell.getValue().toLowerCase()
            return (<Link to={path}><div id="big-table-cell">{cell.getValue()}</div></Link>)
          } else if (header_value === "Weekly Activity") {
            return (<div id="big-table-cell">{cell.getValue() / 1000000}M</div>)
          } else return (<div id="big-table-cell">{cell.getValue()}</div>);
        }
      }))
    }
  )

  const props = { columns: columns, data: data, title: "The Biggest Sentiment Movers 📈" }
  return <SentimentTable {...props} />;
}

export default BiggestSentimentMoversTable;