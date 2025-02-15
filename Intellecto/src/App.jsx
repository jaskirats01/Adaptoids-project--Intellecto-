import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import MicButton from './components/MicButton'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <MicButton />
        
    </>
  )
}

export default App
