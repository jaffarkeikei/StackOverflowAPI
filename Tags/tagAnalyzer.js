const axios = require('axios');
const fs = require('fs');
const process = require('process');

// Function to convert a date string (YYYY-MM-DD) to a Unix timestamp
const toUnixTime = (dateString) => Math.floor(new Date(dateString).getTime() / 1000);

// Fetch popular tags from StackExchange API
const fetchPopularTags = async (fromDate, toDate) => {
  try {
    const response = await axios.get('https://api.stackexchange.com/2.3/tags', {
      params: {
        site: 'stackoverflow',
        fromdate: toUnixTime(fromDate),
        todate: toUnixTime(toDate),
        order: 'desc',
        sort: 'popular',
        pagesize: 10 // Adjust as needed
      }
    });

    // Extend tag information by including the count of questions and the link for each tag
    const tagsInfo = response.data.items.map(item => ({
      name: item.name,
      count: item.count,
      link: `https://stackoverflow.com/tags/${encodeURIComponent(item.name)}/info`
    }));

    console.log('Most Popular Tags:', tagsInfo);
    return tagsInfo;
  } catch (error) {
    console.error(`An error occurred: ${error}`);
    return [];
  }
};

// Save the fetched tags to a JSON file
const saveTagsToFile = (tags, filename) => {
  fs.writeFile(filename, JSON.stringify(tags, null, 2), (err) => {
    if (err) {
      console.error('Error writing to file:', err);
    } else {
      console.log(`Tags saved to ${filename}`);
    }
  });
};

// Main function to run the script
const main = async () => {
  // Example usage: node tagAnalyzer.js 2023-01-01 2023-01-31
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.log('Usage: node tagAnalyzer.js <fromDate> <toDate>');
    return;
  }

  const [fromDate, toDate] = args;
  const tags = await fetchPopularTags(fromDate, toDate);
  if (tags.length > 0) {
    saveTagsToFile(tags, 'popular_tags.json');
  }
};

main();