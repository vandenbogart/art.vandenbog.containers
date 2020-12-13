import React, { useState, useEffect } from 'react';
import { useArticleData, useArticles } from './hooks/articles'

import './dashboard.css'

export const Dashboard = () => {
    const articlesMeta = useArticles();
    const [selectedArticleFilename, setSelectedArticleFilename] = useState(null)
    const selectedArticleData = useArticleData(selectedArticleFilename)

    // Set iframe content when selected article changes
    useEffect(() => {
        if (selectedArticleData && selectedArticleData.data) {
            const iframe = document.getElementById("dashboard__right__page-display")
            iframe.contentWindow.document.open();
            iframe.contentWindow.document.write(selectedArticleData.data.html);
            iframe.contentWindow.document.close();
        }
    }, [selectedArticleData])

    return (
        <div className="dashboard">
            <div className="dashboard__left">
                <div className="dashboard__left__menu">
                    {articlesMeta.data && articlesMeta.data.map(articleMeta => 
                        <div className="dashboard__left__menu__item">
                            <button onClick={() => setSelectedArticleFilename(articleMeta.filename)}>
                                {articleMeta.title}
                            </button>
                        </div>
                    )}

                </div>

            </div>
            <div className="dashboard__right">
                <iframe id="dashboard__right__page-display" className="dashboard__right__page-display-iframe"/>
            </div>

        </div>
    )

}