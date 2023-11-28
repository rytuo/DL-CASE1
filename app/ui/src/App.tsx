import * as React from 'react';
import models, { Coords } from './api/models';
import classNames from 'classnames';
import './App.css'

export interface Sign {
  cls: string,
  xyxy: Coords,
}

export type Signs = Sign[];

function getRndColor() {
  var r = 256*Math.random()|0,
      g = 256*Math.random()|0,
      b = 256*Math.random()|0;
  return 'rgb(' + r + ',' + g + ',' + b + ')';
}

function App() {

  const inputRef = React.useRef<HTMLInputElement>(null);
  const canvasRef = React.useRef<HTMLCanvasElement>(null);

  const [fileUrl, setFileUrl] = React.useState<string>();
  const [signs, setSigns] = React.useState<Signs>();
  const [isLoading, setLoading] = React.useState(false);

  const onFileChange: React.ChangeEventHandler = React.useCallback(e => {
    e.preventDefault();
    if (
      !inputRef.current || // not init
      !inputRef.current.value || // cancel button
      !inputRef.current.files // no files chosen
    ) {
        return;
    }
    const file = inputRef.current.files[0];
    setSigns(undefined);
    setFileUrl(URL.createObjectURL(file));
  }, [inputRef, inputRef.current]);

  const onSubmit: React.FormEventHandler<HTMLFormElement> = React.useCallback(async e => {
    e.preventDefault();
    if (
      !inputRef.current || // not init
      !inputRef.current.value || // cancel button
      !inputRef.current.files // no files chosen
    ) {
        return;
    }
    const file = inputRef.current.files[0];
    setLoading(true);
    const res = await models.image(file);
    setLoading(false);
    const signs = res.items.map(({cls, xyxy}) => ({cls, xyxy}))
    setSigns(signs);
  }, [inputRef, inputRef.current]);


  React.useEffect(() => {
    if (!canvasRef.current || !fileUrl) {
      return;
    }
    const ctx = canvasRef.current.getContext('2d');
    const img = new Image();
    img.onload = () => {
      ctx?.drawImage(img, 0, 0, 640, 480);
    };
    img.src = fileUrl;
  }, [canvasRef, canvasRef.current, fileUrl]);

  React.useEffect(() => {
    if (!canvasRef.current || !signs?.length) {
      return;
    }
    const ctx = canvasRef.current.getContext('2d');
    if (!ctx) {
      return;
    }
    ctx.lineWidth = 2;
    ctx.font = "bold 12px serif";
    for (const sign of signs) {
      const { cls, xyxy } = sign;
      const [x0, y0, x1, y1] = xyxy;
      const w = x1 - x0;
      const h = y1 - y0;

      const color = getRndColor()
      ctx.strokeStyle = color;
      ctx.fillStyle = color;

      ctx.fillText(cls, x0 / 2 - 5, y0 / 2 - 5);

      ctx.beginPath();
      ctx.rect(x0 / 2, y0 / 2, w / 2, h / 2);
      ctx.stroke();
    }
  }, [canvasRef, canvasRef.current, signs]);


  return (
    <div className={classNames('app-container', isLoading && '__loading')}>
      {isLoading && (
        <div className="overlay">
          <div className="spinner"/>
        </div>
      )}

      <h1>Демо-приложение детекции дорожных знаков на фото</h1>
      <form onSubmit={onSubmit} className="form-container">
        <label className="button">
          <input
            type="file"
            name="image"
            accept="image/png, image/gif, image/jpeg"
            className="__hidden"
            onChange={onFileChange}
            ref={inputRef}
          />
          Загрузить фото
        </label>
        <button type='submit'>
          Найти знаки
        </button>
      </form>
      <div>
        <canvas
          ref={canvasRef}
          width={640}
          height={480}
        />
      </div>
    </div>
  )
}

export default App
