import React, { useState, useEffect } from 'react';
import { useArticles } from './hooks/articles'

import './dashboard.css'
import { ArticleViewer } from './ArticleViewer';

export const Dashboard = () => {
    const articlesMeta = useArticles();
    const [selectedArticleIndex, setSelectedArticleIndex] = useState(0)
    // Initially set first article selected
    useEffect(() => {
        if (articlesMeta.data) {
            articlesMeta.data.map((__, j) => {
                const selected = document.getElementById(`menu__item-${j}`)
                selected.classList.remove("dashboard__left__menu__item--selected") 
            })
            const selected = document.getElementById(`menu__item-${selectedArticleIndex}`)
            selected.classList.add("dashboard__left__menu__item--selected")
        }
    }, [articlesMeta.data, selectedArticleIndex])

    return (
        <div className="dashboard">
            <div className="dashboard__left">
                <div className="dashboard__left__menu">
                    <div className="dashboard__left__menu__logo">
                        van
                    </div>
                    <div className="dashboard__left__menu__logo">
                        den
                    </div>
                    <div className="dashboard__left__menu__logo">
                        bog
                    </div>
                    {articlesMeta.data && articlesMeta.data.map((articleMeta, index) => 
                        <div className="dashboard__left__menu__item">
                            <a
                                id={`menu__item-${index}`}
                                className="dashboard__left__menu__item--normal"
                                href=""
                                onClick={(event) => {
                                    event.preventDefault();
                                    setSelectedArticleIndex(index);
                                }}>
                                {articleMeta.title}
                            </a>
                        </div>
                    )}

                </div>

            </div>
            <div className="dashboard__right">
                {articlesMeta.data && <ArticleViewer
                        articlesMeta={articlesMeta}
                        selectedArticleIndex={selectedArticleIndex}
                        setSelectedArticleIndex={setSelectedArticleIndex} />}
            </div>

        </div>
    )

}