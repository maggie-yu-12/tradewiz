import React from 'react';
import { Search } from './Search';

/**
 * Component for greeting message and search on Home Page.
 */
export function HomeSearch() {

  return (
    <div className="search-container">
      <div className="h-greeting">
        <p id="h-main-greeting">Never miss a big stock movement</p>
        <p id="h-sub-greeting">Everything you need for sentiment analysis</p>
        <Search />
      </div>
    </div>
  )
}