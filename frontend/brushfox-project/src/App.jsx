import { useEffect, useState } from 'react'
import axios from 'axios'

function App() {
  const [postsData, setPostsData] = useState([])
  
  const endpoint = `${import.meta.env.VITE_API_URL}/posts/`

  const fetchData = async () => {
    console.log('fetching...')
    const response = await axios.get(endpoint)
    console.log(response)
    const {data} = response
    setPostsData(data)
    console.log(data)
    return data
  }

  const postData = async () => {
    const author = 1
    const title = 'New post API 3'
    const post = 'New post API content 3'
    const slug = 'new-post-api-3'
    
    const body = {
      author,
      title,
      post,
      slug
    }

    const response = await axios.post(endpoint, body)
    console.log(response)
    return response.data
  }

  const hadleSendData = async () => {
    const newData = await postData()
    if (newData) {
      setPostsData(prevState => [...prevState, newData])
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  return (
    <> 
      <ul>
        {postsData.map(el => <li key={el.id}>{el.title}</li>)}
      </ul>
      <button onClick={hadleSendData}>Send data</button>
    </>
  ) 
}

export default App


// to co wcześniej było w App.jsx
// import { useState, useEffect } from 'react'
// import axios from 'axios'

// function App() {
//   const [data, setData] = useState([])

//   useEffect(() => {
//     async function fetchData() {
//       console.log(import.meta.env.VITE_API_URL)
//       try {
//         const response = await fetch(`${import.meta.env.VITE_API_URL}/posts/`)
//         if (!response.ok) {
//           throw new Error('Network response was not ok')
//         }
//         const result = await response.json();
//         console.log(result)
//         setData(result);
//       } catch (error) {
//         console.error('Error fetching data: ', error);
//       }
//     }

//     fetchData()
//   }, []);

//   return (
//     <> 
//       <ul>
//         HELLO WORLD
//         {/* {postsData.map(el => <li key={el.id}>{el.title}</li>)} */}
//       </ul>
//     </>
//   ) 
// }
