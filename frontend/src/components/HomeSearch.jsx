import { Search } from "../pages/Search";

/**
 * Component for greeting message and search on Home Page.
 */
const HomeSearch = () => {
  return (
    <div className="search-container">
      <div className="h-greeting">
        <p id="h-main-greeting">Never miss a big stock movement</p>
        <p id="h-sub-greeting">Everything you need for sentiment analysis</p>
      </div>
      <Search />
    </div>
  )
}

export default HomeSearch;