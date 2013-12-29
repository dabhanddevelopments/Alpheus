
MyCountInBet <- function(R, Upper, Lower, pct = TRUE) {

          R = checkData(R, method = "vector")
          n = length(R)
          counter=0

          for (i in 1:n) 
          {
           if(R[i]>=Lower && R[i]<=Upper) { counter=counter+1 }
          }
          
          if (pct == TRUE) 
            { 
              res=counter/n
            }
          else
            {
              res = counter
            }
          
          return(res)
}

 Myapply.fromstart = function (R, FUN = "mean", gap = 1,...)
 {
      R = checkData(R, method = "zoo")
    columns = ncol(R)
    columnnames = colnames(R)
    for (column in 1:columns) {
        column.Return.calc = zoo(NA, order.by = as.Date(time(R)))
        for (i in gap:length(time(R))) {
            data.zoo = window(R[, column, drop = FALSE], start = start(R),
                end = time(R[i]))
            column.Return.calc[i] = apply(as.matrix(data.zoo[,
                , drop = FALSE]), FUN = FUN, ..., MARGIN = 2)
        }
        if (column == 1)
            Return.calc = column.Return.calc
        else Return.calc = merge(Return.calc, column.Return.calc)
    }
    if (!is.null(ncol(Return.calc)))
        colnames(Return.calc) = columnnames

    index(Return.calc) = index(R)
    return(Return.calc)

 }
 
MyVAR <- function(R, IsSample = TRUE) {

          return(MyStdev(R, IsSample = IsSample)^2)
}

MyStdev <- function(R, IsSample = TRUE) {

          R = checkData(R, method = "vector")
          n = length(R)
    if (!IsSample) {           
          return(sqrt(sum((R-mean(R))^2)/(n)))
    }else {
          return(sqrt(sum((R-mean(R))^2)/(n-1)))
    }
}

MySkewness <- function(R, IsSample = TRUE) {

          R = checkData(R, method = "vector")
          n = length(R)
    if (!IsSample) {                 
          m3 <- sum((R-mean(R))^3)/(n)
          m2 <- sum((R-mean(R))^2)/(n)
        return(m3/sqrt(m2)^3)            
    }else {
          m3 <- sum((R-mean(R))^3)/(n-1)
          m2 <- sum((R-mean(R))^2)/(n-1)
        return((n/(n-2))*(m3/sqrt(m2)^3)) 
    }
}
                  
MyKurtosis <- function(R, IsSample = TRUE, IsExcess = TRUE) {

          R = checkData(R, method = "vector")
          n = length(R)
    if (!IsSample) {                    # if sample =FALSE
          m4 <- sum((R-mean(R))^4)/(n)
          m2 <- sum((R-mean(R))^2)/(n)
        if (!IsExcess) {
        return(m4/sqrt(m2)^4)
        }else {
        return((m4/sqrt(m2)^4)-3)
        }
    }else {
          m4 <- sum((R-mean(R))^4)
          m2 <- sum((R-mean(R))^2)/(n-1)
        if (!IsExcess) {
        return((((n*(n+1))/((n-1)*(n-2)*(n-3)))*(m4/sqrt(m2)^4)) - (3*(n-1)^2)/((n-2)*(n-3)) + 3)
        }else {
        return((((n*(n+1))/((n-1)*(n-2)*(n-3)))*(m4/sqrt(m2)^4)) - (3*(n-1)^2)/((n-2)*(n-3)))
        }
    }
}

MyVaR <- function(R, p = 0.99,  method = "Mean", mu = TRUE, positive = TRUE) {
  
  R = checkData(R, method = "vector")
  zc = qnorm(p)
  
if (method == "Modified") {
  sk = MySkewness(R, IsSample = TRUE)
  k = MyKurtosis(R, IsSample = TRUE, IsExcess = TRUE)
  Zcf = zc + (((zc^2 - 1) * sk)/6) + (((zc^3 - 3 * zc) * k)/24) 
      - ((((2 * zc^3) - 5 * zc) * sk^2)/36)
      if(!mu) {
          if (!positive) {
           MyVaR = - Zcf * MyStdev(R)
           }
           else {
           MyVaR = Zcf * MyStdev(R)
           }
         }
      else {
        if (!positive) {
           MyVaR = mean(R) - Zcf * MyStdev(R)
           }
           else {
           MyVaR = -(mean(R) - Zcf * MyStdev(R))
           }
         }
      
}else {
      if(!mu) {
          if (!positive) {
           MyVaR = - zc * MyStdev(R)
           }
           else {
           MyVaR = zc * MyStdev(R)
           }
         }
      else {
        if (!positive) {
           MyVaR = mean(R) - zc * MyStdev(R)
           }
           else {
           MyVaR = -(mean(R) - zc * MyStdev(R))
           }
         }      
}

        return(MyVaR)
}
       
    MyDDev <- function(R, MARet = 0, AnnFactor = 252, IsSample = TRUE) {

          R = checkData(R, method = "vector")

          A = subset(R, R < MARet/AnnFactor)
          n = length(A)
          nt = length(R)
    if (!IsSample) {
          return(sqrt(AnnFactor)*sqrt(sum((A-MARet/AnnFactor)^2)/(nt)))
    }else {
          return(sqrt(AnnFactor)*sqrt(sum((A-MARet/AnnFactor)^2)/(nt-1)))
    }
}

  MyTE <- function(R, B, IsCentral = TRUE, IsSample = TRUE, AnnFactor = 252) {

          R = checkData(R, method = "vector")
          B = checkData(B, method = "vector")
          X = R - B
          n = length(R)
          
    if (!IsSample) {           
          if (!IsCentral) {
          return(sqrt(AnnFactor * sum((R-B)^2)/(n)))
          } else {
                  return(sqrt(AnnFactor) * MyStdev(X, IsSample=FALSE))
    }
     }else {
          if (!IsCentral) {
          return(sqrt(AnnFactor * sum((R-B)^2)/(n-1)))
          } else {
                  return(sqrt(AnnFactor) * MyStdev(X, IsSample=TRUE))
          }
    }
}
  
  MySharpe <- function(R, MARet = 0, AnnFactor = 252, IsSample = TRUE, IsAdj = FALSE, IsGeo = TRUE) {
  
    R = checkData(R-MARet, method = "vector")
    Num = Return.annualized(R, scale = AnnFactor, geometric = IsGeo)
    Den = MyStdev(R, IsSample = IsSample)*sqrt(AnnFactor)
    
    return(Num/Den)
        
  }
  
  MyMSharpe <- function(R, MARet = 0, p=0.99, IsGeo = TRUE) {
  
    R = checkData(R-MARet, method = "vector")
    Num = Return.cumulative(R, geometric = IsGeo)  
    Den = MyVaR(R, p = p,  method = "Modified", mu = FALSE, positive = TRUE) 
    
    return(Num/Den)
    
  }
  
  MySortino <- function(R, MARet = 0, AnnFactor = 252, IsSample = TRUE, IsAdj = FALSE, IsGeo = TRUE) {
  
    R = checkData(R-MARet, method = "vector")
    
    Num = Return.annualized(R, scale = AnnFactor, geometric = IsGeo)
    Den = MyDDev(R, MARet = MARet, AnnFactor = AnnFactor, IsSample = IsSample)
    
    return(Num/Den)
    
  }
  
  RiskReturnDecomp <- function(R, B, AnnFactor = 252, geometric = TRUE, RegStats = FALSE) {
   #not used in any report
   
          R = checkData(R, method = "vector")
          B = checkData(B, method = "vector")
          X = R - B
          n = length(R)
          
          CFRet = Return.cumulative(R, geometric = geometric)
          CBRet = Return.cumulative(B, geometric = geometric)
          ERet = CFRet - CBRet
          
          MFRet = mean(R)
          MBRet = mean(B)
          FVAR = MyVAR(R,IsSample=FALSE)
          BVAR = MyVAR(B,IsSample=FALSE)
          TE = MyTE(R, B, IsCentral = FALSE, IsSample = FALSE, AnnFactor = AnnFactor)
          
          model.lm = lm(R ~ B)
          AdjRSQ = summary(model.lm)[[9]]
          RESID.VAR = MyVAR(summary(model.lm)[[3]],IsSample=FALSE)
          ST.ERROR = summary(model.lm)[[6]]
          ALPHA = coef(model.lm)[[1]]
          ALPHA.P = summary(model.lm)$coefficients[1, 4]
          ALPHA.SE = summary(model.lm)$coefficients[1, 2]
          BETA = coef(model.lm)[[2]]
          BETA.P = summary(model.lm)$coefficients[2, 4]
          BETA.SE = summary(model.lm)$coefficients[2, 2]
         
          R1 = c(CFRet,ERet,TE)
          R2 = c(ALPHA*n,ALPHA*n,(ALPHA^2)*AnnFactor/TE)
          R3 = c(BETA*CBRet, (BETA-1)*CBRet, ((BETA-1)^2)*(BVAR+MBRet^2)*AnnFactor/TE)
          R4 = c(CFRet -  (ALPHA*n +BETA*CBRet),ERet - (ALPHA*n + (BETA-1)*CBRet), RESID.VAR*AnnFactor/TE )
          R5 = c("-","-",(2*ALPHA*(BETA-1)*MBRet)* AnnFactor/TE)

          
          if (!RegStats) { A = rbind(R1,R2,R3,R4,R5)
                          MT.R.Names = c("Total","Alpha", "Beta", "Residual","Crossterm")
                          MT.C.Names = c("Portfolio Return","Active Return","Tracking Error")
                          rownames(A) = MT.R.Names
                          colnames(A) = MT.C.Names
          } else { A = cbind(AdjRSQ, ST.ERROR, ALPHA, ALPHA.P, ALPHA.SE, BETA, BETA.P, BETA.SE)
                          ST.C.Names = c("Adj R-Squared", "Residual Std Error", "ALPHA", "ALPHA p-value", "ALPHA Std Error", "BETA", "BETA p-value", "BETA Std Error")
                          colnames(A) = ST.C.Names
          }
          
          return(A)
  }   
  
  RollRiskReturnDecomp <- function(R, B, AnnFactor = 252, geometric = TRUE, RegStats = FALSE, By = 1, Width, Res = 3) {
    
       #not used in any report
    Ra = checkData(R, method = "zoo")
    Rb = checkData(B, method = "zoo")
    columns.a = ncol(Ra)
    columns.b = ncol(Rb)
    columnnames.a = colnames(Ra)
    columnnames.b = colnames(Rb)
    Ra.excess = Return.excess(Ra, 0)
    Rb.excess = Return.excess(Rb, 0)
    for (column.a in 1:columns.a) {
        for (column.b in 1:columns.b) {
            merged.assets = merge(Ra.excess[, column.a, drop = FALSE],
                Rb.excess[, column.b, drop = FALSE])
                
                if (RegStats == FALSE) {
                column.result = rollapply(na.omit(merged.assets[,
                  , drop = FALSE]), width = Width, FUN = function(x) RiskReturnDecomp(x[,
                  1, drop = FALSE], x[, 2, drop = FALSE], AnnFactor = AnnFactor, geometric = geometric, RegStats = FALSE)[,Res],
                  by = By, by.column = FALSE, align = "right")
                  } else {
                  column.result = rollapply(na.omit(merged.assets[,
                  , drop = FALSE]), width = Width, FUN = function(x) RiskReturnDecomp(x[,
                  1, drop = FALSE], x[, 2, drop = FALSE], AnnFactor = AnnFactor, geometric = geometric, RegStats = TRUE)[1,],
                  by = By, by.column = FALSE, align = "right")                
                  }
      }
    }
    
    return(column.result)
    }
    
    RiskReturn <- function(R, B, AnnFactor = 252, geometric = TRUE, IsCentral = TRUE, IsSample = TRUE) {
    
          R = checkData(R, method = "vector")
          B = checkData(B, method = "vector")
          X = R - B
          
          CFRet = Return.cumulative(R, geometric = geometric)
          CBRet = Return.cumulative(B, geometric = geometric)
          ERet = CFRet - CBRet
          FVol = sqrt(AnnFactor)*MyStdev(R,IsSample=IsSample)
          BVol = sqrt(AnnFactor)*MyStdev(B,IsSample=IsSample)
          TE = MyTE(R, B, IsCentral = IsCentral, IsSample = IsSample, AnnFactor = AnnFactor)
          
          A = cbind(CFRet,FVol,CBRet,BVol,ERet,TE)
          MT.C.Names = c("Portfolio Return","Portfolio Volatility","Benchmark Return","Benchmark Volatility","Active Return","Tracking Error")
          colnames(A) = MT.C.Names
    
    return(A)
    }
    
    RollRiskReturn <- function(R, B, AnnFactor = 252, geometric = TRUE, IsCentral = TRUE, IsSample = TRUE, By = 1, Width, IsActive = TRUE) {
    
    Ra = checkData(R, method = "zoo")
    Rb = checkData(B, method = "zoo")
    columns.a = ncol(Ra)
    columns.b = ncol(Rb)
    columnnames.a = colnames(Ra)
    columnnames.b = colnames(Rb)
    Ra.excess = Return.excess(Ra, 0)
    Rb.excess = Return.excess(Rb, 0)
    for (column.a in 1:columns.a) {
        for (column.b in 1:columns.b) {
            merged.assets = merge(Ra.excess[, column.a, drop = FALSE],
                Rb.excess[, column.b, drop = FALSE])
                
                if (IsActive == FALSE) {
                column.result = rollapply(na.omit(merged.assets[,
                  , drop = FALSE]), width = Width, FUN = function(x) RiskReturn(x[,
                  1, drop = FALSE], x[, 2, drop = FALSE], AnnFactor = AnnFactor, geometric = geometric, IsCentral = IsCentral, IsSample = IsSample)[,1:4],
                  by = By, by.column = FALSE, align = "right")
                  } else {
                  column.result = rollapply(na.omit(merged.assets[,
                  , drop = FALSE]), width = Width, FUN = function(x) RiskReturn(x[,
                  1, drop = FALSE], x[, 2, drop = FALSE], AnnFactor = AnnFactor, geometric = geometric, IsCentral = IsCentral, IsSample = IsSample)[,5:6],
                  by = By, by.column = FALSE, align = "right")                
                  }
      }
    }
    return(column.result)
    }
    
     
      FamaDecomposition <- function(R, B, AnnFactor = 252, geometric = TRUE, IsSample = TRUE, RiskFree = 0) {
  
          R = checkData(R, method = "vector")
          B = checkData(B, method = "vector")
          X = R - B
          n = length(R)
          
          R.excess = Return.excess(R, RiskFree/AnnFactor)
          B.excess = Return.excess(B, RiskFree/AnnFactor)
          
          CFRet = Return.cumulative(R, geometric = geometric)
          CBRet = Return.cumulative(B, geometric = geometric)
          CRFRet = -1 + (1+RiskFree/AnnFactor)^(n)          
          ERet = CFRet - CBRet

          FVAR = MyVAR(R,IsSample=TRUE)    
          BVAR = MyVAR(B,IsSample=TRUE)
          BETAF = sqrt(FVAR/BVAR)
          
          model.lm = lm(R.excess ~ B.excess)
          BETA = coef(model.lm)[[2]]
          
          
          MarketT = BETA*(CBRet-CRFRet)
          MarketA = (BETA - 1)*(CBRet-CRFRet)
          Selectivity = (CFRet-CRFRet)-BETA*(CBRet-CRFRet)
          Diversification = (BETAF-BETA)*(CBRet-CRFRet)
          NetSelectivity = Selectivity - Diversification
          
          
          R1 = c(CFRet - CRFRet, MarketT, Selectivity, Diversification, NetSelectivity)
          R2 = c(ERet, MarketA, Selectivity, Diversification, NetSelectivity)

                A = cbind(R1,R2)
                MT.R.Names = c("Total","Allocation / Systematic Risk", "Selectivity", "Diversification","Net Selectivity")
                MT.C.Names = c("Total Risk Premium","Active Return")
                rownames(A) = MT.R.Names
                colnames(A) = MT.C.Names
          
          return(A)
  }
  
  
  TEDecomp <- function(R, B, AnnFactor = 252) {
  
          
          R = checkData(R, method = "vector")
          B = checkData(B, method = "vector")
          MFRet = mean(R)
          MBRet = mean(B)
          FVAR = MyVAR(R,IsSample=FALSE)
          BVAR = MyVAR(B,IsSample=FALSE)
          cTE = MyTE(R, B, IsCentral = TRUE, IsSample = TRUE, AnnFactor = AnnFactor)
          ncTE = MyTE(R, B, IsCentral = FALSE, IsSample = FALSE, AnnFactor = AnnFactor)
          
          model.lm = lm(R ~ B)
          RESID.VAR = MyVAR(summary(model.lm)[[3]],IsSample=FALSE)
          ALPHA = coef(model.lm)[[1]]
          BETA = coef(model.lm)[[2]]

          R1 = cTE
          R2 = ncTE
          R3 = c((ALPHA^2)*AnnFactor/ncTE)
          R4 = c(((BETA-1)^2)*(BVAR+MBRet^2)*AnnFactor/ncTE)
          R5 = c(RESID.VAR*AnnFactor/ncTE )
          R6 = c((2*ALPHA*(BETA-1)*MBRet)* AnnFactor/ncTE)

          
          A = rbind(R1,R2,R3,R4,R5,R6)
          
          MT.R.Names = c("Central Tracking Error", "Non Central Tracking Error", "Alpha Component", "Beta Component", "Residual Component", "Crossterm Component")
          rownames(A) = MT.R.Names          
          return(A)                  
  }   
  
  RollTEDecomp <- function(R, B, AnnFactor = 252, By = 1, Width = 66) {
    
    Ra = checkData(R, method = "zoo")
    Rb = checkData(B, method = "zoo")
    columns.a = ncol(Ra)
    columns.b = ncol(Rb)
    columnnames.a = colnames(Ra)
    columnnames.b = colnames(Rb)
    for (column.a in 1:columns.a) {
        for (column.b in 1:columns.b) {
            merged.assets = merge(Ra[, column.a, drop = FALSE],
                Rb[, column.b, drop = FALSE])
                
                column.result = rollapply(na.omit(merged.assets[,
                  , drop = FALSE]), width = Width, FUN = function(x) TEDecomp(x[,
                  1, drop = FALSE], x[, 2, drop = FALSE], AnnFactor = AnnFactor),
                  by = By, by.column = FALSE, align = "right")
              
        MT.C.Names = c("Central Tracking Error", "Non Central Tracking Error", "Alpha Component", "Beta Component", "Residual Component", "Crossterm Component")
        colnames(column.result) = MT.C.Names
      }
    }  
    
    return(column.result)
    }

    
    RiskReturn <- function(R, B, AnnFactor = 252, geometric = TRUE, IsCentral = TRUE, IsSample = TRUE) {
    
          R = checkData(R, method = "vector")
          B = checkData(B, method = "vector")
          X = R - B
          
          CFRet = Return.cumulative(R, geometric = geometric)
          CBRet = Return.cumulative(B, geometric = geometric)
          ERet = CFRet - CBRet
          FVol = sqrt(AnnFactor)*MyStdev(R,IsSample=IsSample)
          BVol = sqrt(AnnFactor)*MyStdev(B,IsSample=IsSample)
          TE = MyTE(R, B, IsCentral = IsCentral, IsSample = IsSample, AnnFactor = AnnFactor)
          Cor = cor(R,B)
          
          A = cbind(CFRet,FVol,CBRet,BVol,ERet,TE,Cor)
          MT.C.Names = c("Portfolio Return","Portfolio Volatility","Benchmark Return","Benchmark Volatility","Active Return","Tracking Error", "Correlation")
          colnames(A) = MT.C.Names
    
    return(A)
    }
    
    RollRiskReturn <- function(R, B, AnnFactor = 252, geometric = TRUE, IsCentral = TRUE, IsSample = TRUE, By = 1, Width = 66, IsActive = TRUE) {
    
    Ra = checkData(R, method = "zoo")
    Rb = checkData(B, method = "zoo")
    columns.a = ncol(Ra)
    columns.b = ncol(Rb)
    columnnames.a = colnames(Ra)
    columnnames.b = colnames(Rb)
    Ra.excess = Return.excess(Ra, 0)
    Rb.excess = Return.excess(Rb, 0)
    for (column.a in 1:columns.a) {
        for (column.b in 1:columns.b) {
            merged.assets = merge(Ra.excess[, column.a, drop = FALSE],
                Rb.excess[, column.b, drop = FALSE])
                
                if (IsActive == FALSE) {
                column.result = rollapply(na.omit(merged.assets[,
                  , drop = FALSE]), width = Width, FUN = function(x) RiskReturn(x[,
                  1, drop = FALSE], x[, 2, drop = FALSE], AnnFactor = AnnFactor, geometric = geometric, IsCentral = IsCentral, IsSample = IsSample)[,1:4],
                  by = By, by.column = FALSE, align = "right")
                  } else {
                  column.result = rollapply(na.omit(merged.assets[,
                  , drop = FALSE]), width = Width, FUN = function(x) RiskReturn(x[,
                  1, drop = FALSE], x[, 2, drop = FALSE], AnnFactor = AnnFactor, geometric = geometric, IsCentral = IsCentral, IsSample = IsSample)[,5:7],
                  by = By, by.column = FALSE, align = "right")                
                  }
      }
    }
    return(column.result)
    }
    
     
          ReturnDecomposition <- function(R, B, AnnFactor = 252, geometric = TRUE, RiskFree = 0, SelDecomp = TRUE) {
          #Based on Fama decomposition
          
          R = checkData(R, method = "vector")
          B = checkData(B, method = "vector")
          X = R - B
          n = length(R)
    
          R.excess = Return.excess(R, RiskFree/AnnFactor)
          B.excess = Return.excess(B, RiskFree/AnnFactor)
          
          CFRet = Return.cumulative(R, geometric = geometric)
          CBRet = Return.cumulative(B, geometric = geometric)
          CRFRet = (RiskFree/AnnFactor)*(n)
          ERet = CFRet - CBRet

          FVAR = MyVAR(R,IsSample=TRUE)    
          BVAR = MyVAR(B,IsSample=TRUE)
          BETAF = sqrt(FVAR/BVAR)
          
          model.lm = lm(R.excess ~ B.excess)
          BETA = coef(model.lm)[[2]]
          
          MarketT = BETA*(CBRet-CRFRet)
          MarketA = (BETA - 1)*(CBRet-CRFRet)
          Selectivity = (CFRet-CRFRet)-BETA*(CBRet-CRFRet)
          Diversification = (BETAF-BETA)*(CBRet-CRFRet)
          NetSelectivity = Selectivity - Diversification
          
          if (SelDecomp == TRUE) {
          R1 = c(CFRet - CRFRet, MarketT, Selectivity, Diversification, NetSelectivity)
          R2 = c(ERet, MarketA, Selectivity, Diversification, NetSelectivity)

                A = cbind(R1,R2)
                MT.R.Names = c("Total","Allocation / Systematic Risk", "Selectivity", "Diversification","Net Selectivity")
                MT.C.Names = c("Total Risk Premium","Active Return")
                rownames(A) = MT.R.Names
                colnames(A) = MT.C.Names
          } else {
          R1 = c(CFRet - CRFRet, MarketT, Selectivity)
          R2 = c(ERet, MarketA, Selectivity)
                A = cbind(R1,R2)
                MT.R.Names = c("Total","Allocation / Systematic Risk", "Selectivity")
                MT.C.Names = c("Total Risk Premium","Active Return")
                rownames(A) = MT.R.Names
                colnames(A) = MT.C.Names
          }
          
          return(A)
  }       
  
          ReturnDecompositionRoll <- function(R, B, AnnFactor = 252, geometric = TRUE, RiskFree = 0, SelDecomp = TRUE, By = 1, Width = 66, IsActive = TRUE) {
          Ra = checkData(R, method = "zoo")
          Rb = checkData(B, method = "zoo")
          columns.a = ncol(Ra)
          columns.b = ncol(Rb)
          columnnames.a = colnames(Ra)
          columnnames.b = colnames(Rb)
          for (column.a in 1:columns.a) {
          for (column.b in 1:columns.b) {
            merged.assets = merge(Ra[, column.a, drop = FALSE],
                Rb[, column.b, drop = FALSE])
                
                if (IsActive == FALSE) {
                column.result = rollapply(na.omit(merged.assets[,
                  , drop = FALSE]), width = Width, FUN = function(x) ReturnDecomposition(x[,
                  1, drop = FALSE], x[, 2, drop = FALSE], AnnFactor = AnnFactor, geometric = geometric, RiskFree = RiskFree, SelDecomp = SelDecomp)[,1],
                  by = By, by.column = FALSE, align = "right")
                  } else {
                  column.result = rollapply(na.omit(merged.assets[,
                  , drop = FALSE]), width = Width, FUN = function(x) ReturnDecomposition(x[,
                  1, drop = FALSE], x[, 2, drop = FALSE], AnnFactor = AnnFactor, geometric = geometric, RiskFree = RiskFree, SelDecomp = SelDecomp)[,2],
                  by = By, by.column = FALSE, align = "right") 
                  }
      }
    }
    return(column.result)
    }
          #MarketModel
          
          MarketModel <- function(R, B, RiskFree = 0, AnnFactor = 252)   {
          
          R = checkData(R, method = "vector")
          B = checkData(B, method = "vector")
          R.excess = Return.excess(R, RiskFree/AnnFactor)
          B.excess = Return.excess(B, RiskFree/AnnFactor)
          
          model.lm = lm(R.excess ~ B.excess)
          AdjRSQ = summary(model.lm)[[9]]
          RESID.VAR = MyVAR(summary(model.lm)[[3]],IsSample=FALSE)
          ST.ERROR = summary(model.lm)[[6]]
          ALPHA = coef(model.lm)[[1]]
          ALPHA.P = summary(model.lm)$coefficients[1, 4]
          ALPHA.SE = summary(model.lm)$coefficients[1, 2]
          BETA = coef(model.lm)[[2]]
          BETA.P = summary(model.lm)$coefficients[2, 4]
          BETA.SE = summary(model.lm)$coefficients[2, 2]
         
          
         
         A = cbind(AdjRSQ, ST.ERROR, ALPHA, ALPHA.P, ALPHA.SE, BETA, BETA.P, BETA.SE)
                          ST.C.Names = c("Adj R-Squared", "Residual Std Error", "ALPHA", "ALPHA p-value", "ALPHA Std Error", "BETA", "BETA p-value", "BETA Std Error")
                          colnames(A) = ST.C.Names
           return(A)
  
          }
  
          MarketModelRoll <- function(R, B, RiskFree = 0, AnnFactor = 252, By = 1, Width = 66)   {
          
          Ra = checkData(R, method = "xts")
          Rb = checkData(B, method = "xts")
          columns.a = ncol(Ra)
          columns.b = ncol(Rb)
          columnnames.a = colnames(Ra)
          columnnames.b = colnames(Rb)
          for (column.a in 1:columns.a) {
          for (column.b in 1:columns.b) {
            merged.assets = merge(Ra[, column.a, drop = FALSE],
                Rb[, column.b, drop = FALSE])
                

                column.result = rollapply(na.omit(merged.assets[,
                  , drop = FALSE]), width = Width, FUN = function(x) MarketModel(x[,
                  1, drop = FALSE], x[, 2, drop = FALSE], AnnFactor = AnnFactor, RiskFree = RiskFree),
                  by = By, by.column = FALSE, align = "right")
                  
                  ST.C.Names = c("Adj R-Squared", "Residual Std Error", "ALPHA", "ALPHA p-value", "ALPHA Std Error", "BETA", "BETA p-value", "BETA Std Error")
                  colnames(column.result) = ST.C.Names
        } 
      }
    
    return(column.result)
    
    }      
          TraynorMazuyModel <- function(R, B, RiskFree = 0, AnnFactor = 252)   {
          
          R = checkData(R, method = "vector")
          B = checkData(B, method = "vector")
          R.excess = Return.excess(R, RiskFree/AnnFactor)
          B.excess = Return.excess(B, RiskFree/AnnFactor)
          B.excessSQ = B.excess^2
          
          
           merged.zMT = na.omit(merge(R.excess, B.excess, B.excessSQ))
           merged.dfMT = as.data.frame(merged.zMT)
           colnames(merged.dfMT) = c("Asset.excess", "Index.excess", "Index.excessSQ")
           model.lmMT = lm(R.excess ~ B.excess + B.excessSQ, merged.dfMT)          
          
          AdjRSQ = summary(model.lmMT)[[9]]
          RESID.VAR = MyVAR(summary(model.lmMT)[[3]],IsSample=FALSE)
          ST.ERROR = summary(model.lmMT)[[6]]
          ALPHA = coef(model.lmMT)[[1]]
          ALPHA.P = summary(model.lmMT)$coefficients[1, 4]
          ALPHA.SE = summary(model.lmMT)$coefficients[1, 2]
          BETA = coef(model.lmMT)[[2]]
          BETA.P = summary(model.lmMT)$coefficients[2, 4]
          BETA.SE = summary(model.lmMT)$coefficients[2, 2]
          TMBETA = coef(model.lmMT)[[3]]
          TMBETA.P = summary(model.lmMT)$coefficients[3, 4]
          TMBETA.SE = summary(model.lmMT)$coefficients[3, 2]
         
          A = cbind(AdjRSQ, ST.ERROR, ALPHA, ALPHA.P, ALPHA.SE, BETA, BETA.P, BETA.SE, TMBETA, TMBETA.P, TMBETA.SE)
          ST.C.Names = c("Adj R-Squared", "Residual Std Error", "ALPHA", "ALPHA p-value", "ALPHA Std Error", "BETA", "BETA p-value", "BETA Std Error", "MTBETA", "MTBETA p-value", "MTBETA Std Error")
                          colnames(A) = ST.C.Names
           return(A)
          }
          
         TraynorMazuyModelRoll <- function(R, B, RiskFree = 0, AnnFactor = 252, By = 1, Width = 66)  {
         
          Ra = checkData(R, method = "zoo")
          Rb = checkData(B, method = "zoo")
          columns.a = ncol(Ra)
          columns.b = ncol(Rb)
          columnnames.a = colnames(Ra)
          columnnames.b = colnames(Rb)
          for (column.a in 1:columns.a) {
          for (column.b in 1:columns.b) {
            merged.assets = merge(Ra[, column.a, drop = FALSE],
                Rb[, column.b, drop = FALSE])
                

                column.result = rollapply(na.omit(merged.assets[,
                  , drop = FALSE]), width = Width, FUN = function(x) TraynorMazuyModel(x[,
                  1, drop = FALSE], x[, 2, drop = FALSE], AnnFactor = AnnFactor, RiskFree = RiskFree),
                  by = By, by.column = FALSE, align = "right")
                  
                  ST.C.Names = c("Adj R-Squared", "Residual Std Error", "ALPHA", "ALPHA p-value", "ALPHA Std Error", "BETA", "BETA p-value", "BETA Std Error", "MTBETA", "MTBETA p-value", "MTBETA Std Error")
                  colnames(column.result) = ST.C.Names
        } 
      }
       return(column.result)
       }
       
       
       MyBaseMetrics <- function(R, MM = c("Sum", "Average", "MStDev")) {
        
        R  = checkData(R, method = "xts")
        
        if(MM == "Sum"){ MyMetricsBase = sum(R) }
        if(MM == "Average"){ MyMetricsBase = mean(R) }
        
        if(MM == "MStDev"){ MyMetricsBase = MyStdev(R, IsSample = TRUE) }
        
        return( MyMetricsBase  )
        }
        
        MyBaseMetricsRoll <- function(R, mm = c("Sum", "Average", "MStDev"), By = 1, Width = 66) 
        {
         
          R = checkData(R, method = "xts") 
          column.result = rollapply(R, width = Width, FUN = function(x) MyBaseMetrics(x, MM = mm), by = By, by.column = FALSE, align = "right")
          
          return(column.result)
       
        }
        
               
        MyMetricsI <- function(R, AnnFactor = 252, MM = c("MCFRet", "MAnRet", "MStDev", "MDDev", "MSkew", "MKurt", "MVaR", "MMDD", "MOmega", "MSharpe", "MMSharpe", "MSortino", "MFlat" )) {
        
        R  = checkData(R, method = "xts")
        
        if(MM == "MCFRet"){ MyMetricsI = Return.cumulative(R, geometric = TRUE) }
        if(MM == "MAnRet"){ MyMetricsI = Return.annualized(R, scale = AnnFactor, geometric = TRUE) }
        
        if(MM == "MStDev"){ MyMetricsI = MyStdev(R, IsSample = TRUE)*(AnnFactor)^0.5 }
        if(MM == "MDDev"){ MyMetricsI = MyDDev(R, MARet = 0, AnnFactor = AnnFactor, IsSample = TRUE) }
        
        if(MM == "MSkew"){ MyMetricsI = MySkewness(R, IsSample = TRUE) }
        if(MM == "MKurt"){ MyMetricsI = MyKurtosis(R, IsSample = TRUE, IsExcess = TRUE) }
        if(MM == "MVaR"){ MyMetricsI = MyVaR(R, p = 0.99,  method = "Mean", mu = TRUE, positive = TRUE) }
        
        if(MM == "MMDD"){ MyMetricsI = maxDrawdown(R, weights=NULL, geometric = TRUE)}
        
        if(MM == "MOmega"){ MyMetricsI = Omega(R,method="interp",output="point") }
        
        if(MM == "MSharpe")  { MyMetricsI = MySharpe(R, MARet = 0, AnnFactor = AnnFactor, IsSample = TRUE, IsAdj = FALSE, IsGeo = TRUE)}
        if(MM == "MMSharpe")  { MyMetricsI =MyMSharpe(R, MARet = 0, p = 0.99, IsGeo = TRUE)}
        if(MM == "MSortino") { MyMetricsI = MySortino(R, MARet = 0, AnnFactor = AnnFactor, IsSample = TRUE, IsAdj = FALSE, IsGeo = TRUE)}
        
        if(MM == "MFlat") { MyMetricsI = MyCountInBet(R, 0, 0)}
        
        return( MyMetricsI  )
        }
        
      
        MyMetricsIRoll <- function(R, AnnFactor = 252, mm = c("MCFRet", "MAnRet", "MStDev", "MDDev", "MSkew", "MKurt", "MVaR", "MMDD", "MOmega", "MSharpe", "MMSharpe", "MSortino", "MFlat" ), By = 1, Width = 66) 
        {
         
          R = checkData(R, method = "xts") 
          column.result = rollapply(R, width = Width, FUN = function(x) MyMetricsI(x, AnnFactor=AnnFactor, MM = mm), by = By, by.column = FALSE, align = "right")
          
          return(column.result)
       
        }
        
        
    CPos <- function(R)    {
                #returns positive pct in a numeric column
          R = checkData(R, method = "vector")
          n = length(R)
          MyOnes = ifelse(R>0,1,0)
    
          return(sum(MyOnes)/n)
    
    }
