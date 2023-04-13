import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import * as React from 'react';
import { FixedSizeList } from 'react-window';



export const FavoritesList = ({ favorites, setSelectedCompany }) => {
  function handleListItemClick(event, company) {
    setSelectedCompany(company)
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
  return (
    <Box
      sx={{ width: '100%', height: '100%', maxWidth: '90%', bgcolor: 'transparent' }}
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