import React from 'react'
import { Link } from "react-router-dom";
import Button from '@mui/material/Button';


const Home = () => {
	return (
		<div className='chatbot no-scroll' style={{
			// backgroundColor: "red",
		}}>
			<div class="two alt-two" style={{
				paddingTop: '4rem',
				color: "white"
			}}>
				<h1>Mascir chatbot
					<span>A chatbot dedicated for elderly care</span>
				</h1>
				<div style={{
					color: "rgb(91, 97, 102)",
					fontSize: "18px",
					marginTop: "100px",
					textAlign: "justify"
				}}><p>
						Lorem ipsum dolor sit amet. Eum odit minus a assumenda rerum est voluptatem minus est nihil maxime et accusantium consequatur qui dolorum asperiores. Aut dolor dolores ut quis commodi et accusamus deleniti qui optio internos est necessitatibus recusandae eum delectus voluptatibus. Et ipsam odio ea aliquid debitis 33 galisum repellendus vel beatae amet. Quo ducimus natus est repellat vero quo recusandae nostrum vel odio excepturi suscipit veniam.
					</p>
				</div>
				<div style={{
					display: "grid",
					padding: "2rem",
					paddingLeft: "8rem",
					paddingRight: "8rem"
				}}>
					<Button variant="contained" size='large' className="main-btn"><Link to="/chatbot">Start chatting</Link></Button>
				</div>
			</div>
		</div>
	)
}

export default Home