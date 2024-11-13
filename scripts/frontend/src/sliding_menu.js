import React, { useState, useEffect, useRef } from "react";
import Slider from "react-slick";
import "./sliding_menu.css";

const slides = [
    { text: "Welcome to the FPL Player Scores tool! Staytuned for updates of the latest data."},
    { text: "Did you know? The scores of the different positions is not comparable!"},
    { text: "Stay ahead in FPL, get on players performing the best before everyone else in your mini league!"},
];

function Sliding_menu() {
    const settings = {
        dots: true,
        infinite: true, 
        autoplay: true, 
        autplaySpeed: 8000,
        pauseOnHover: true,
        arrows: false,
    };

    const [curr_slide, set_curr_slide] = useState(0);
    const interval_id = useRef(null); // storting the id of interval

    // automatic transition between slides
    useEffect(() => {
        start_auto_slide();

        return () => clearInterval(interval_id.current)
    }, []);

    const start_auto_slide = () => {
        clearInterval(interval_id.current); // clear any existing intervals
        interval_id.current = setInterval(() => {
            set_curr_slide((prev_slide) => (prev_slide + 1) % slides.length) // can wrap to the start if end is reached
        }, 8000); // 8 seconds for each slide
    };

    // manually go to the next slide 
    const go_to_slide = (index) => {
        set_curr_slide(index);
        start_auto_slide(); // restart the interval
    }

    return (
        <div className="sliding-menu">
            <div className="slide-content">
                <h3>{slides[curr_slide].text}</h3>
            </div>

            <div className="navigation-dots">
                {slides.map((_, index) => (
                    <span
                    key={index}
                    className={`dot ${index === curr_slide ? 'active' : ''}`} // needs to give the active dot, both dot class and active dot class
                    onClick={() => go_to_slide(index)} 
                    ></span>
                ))}
            </div>
        </div>
    );
}

export default Sliding_menu;