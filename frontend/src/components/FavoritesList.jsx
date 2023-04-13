import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import * as React from 'react';
import { FixedSizeList } from 'react-window';

function handleListItemClick(event, company) {
  console.log(event)
}

function renderRow(props) {
  console.log(props)
  const { data, index, style } = props;

  style.height = 80
  style.padding = 0
  style.margin = 0
  style.width = '90%'
  return (
    <ListItem style={style} key={index} component="div" disablePadding>
      <ListItemButton onClick={(e) => handleListItemClick(e, data[index])}>
        <ListItemText>
          <p id="favorite-item">{"#" + data[index]}</p>
        </ListItemText>
      </ListItemButton>
    </ListItem>
  );
}

export const FavoritesList = ({ favorites }) => {
  console.log(favorites)
  return (
    <Box
      sx={{ width: '100%', height: 450, maxWidth: '90%', bgcolor: 'transparent' }}
    >
      <FixedSizeList
        height={450}
        width={400}
        itemSize={60}
        itemCount={favorites.length}
        overscanCount={5}
        itemData={favorites}
      >
        {renderRow}
      </FixedSizeList>
    </Box>
  );
}