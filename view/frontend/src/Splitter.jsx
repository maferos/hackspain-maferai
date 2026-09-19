// A drag handle between two views. "col" is a vertical bar dragged left/right,
// "row" a horizontal bar dragged up/down. onStart(bar) runs when the drag
// begins (measure the parent there) and returns a function that receives how
// far the pointer has moved along the axis, in pixels. Double-click resets.

export default function Splitter({ direction, onStart, onReset }) {
  const handlePointerDown = (event) => {
    if (event.button !== 0) return;
    event.preventDefault();
    const bar = event.currentTarget;
    const axis = (e) => (direction === "col" ? e.clientX : e.clientY);
    const origin = axis(event);
    const move = onStart(bar);

    const handleMove = (e) => move(axis(e) - origin);
    const handleUp = () => {
      bar.removeEventListener("pointermove", handleMove);
      bar.removeEventListener("pointerup", handleUp);
      bar.removeEventListener("pointercancel", handleUp);
      bar.classList.remove("splitter--dragging");
      document.body.classList.remove(`resizing-${direction}`);
    };

    bar.setPointerCapture(event.pointerId);
    bar.classList.add("splitter--dragging");
    document.body.classList.add(`resizing-${direction}`);
    bar.addEventListener("pointermove", handleMove);
    bar.addEventListener("pointerup", handleUp);
    bar.addEventListener("pointercancel", handleUp);
  };

  return (
    <div
      className={`splitter splitter--${direction}`}
      role="separator"
      aria-orientation={direction === "col" ? "vertical" : "horizontal"}
      title="Drag to resize · double-click to reset"
      onPointerDown={handlePointerDown}
      onDoubleClick={onReset}
    />
  );
}
