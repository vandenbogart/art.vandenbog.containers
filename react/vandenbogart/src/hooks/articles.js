import { useEffect, useState } from 'react';

export const useArticleData = (filename) => {
    const [ response, setResponse ] = useState({
        error: null,
        status: 'loading',
        data: null
    })
    useEffect(() => {
        if (filename !== null) {
            fetch(`/articles/${filename}`).then((response) => {
                return response.json()
            })
                .then((resObj) => {
                    setResponse({
                        error: null,
                        status: 'ok',
                        data: resObj
                    })
                })
                .catch((error) => {
                    setResponse({
                        error: error,
                        status: 'bad',
                        data: null,
                    })
                })
        }
        
    }, [filename])
    return response
}

export const useArticles = () => {
    const [ response, setResponse ] = useState({
        error: null,
        status: 'loading',
        data: null
    })
    useEffect(() => {
        fetch('/articles').then((response) => {
            return response.json()
        })
            .then((resObj) => {
                setResponse({
                    error: null,
                    status: 'ok',
                    data: resObj.articles
                })
            })
            .catch((error) => {
                setResponse({
                    error: error,
                    status: 'bad',
                    data: null,
                })
            })
        
    }, [])
    return response
}